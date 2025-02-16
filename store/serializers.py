from itertools import product

from django.db import transaction
from rest_framework import serializers
from decimal import Decimal
from store.models import Product, Collection, Review, Cart, CartItem, Customer, Order, OrderItem
from store.signals import order_created


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory', 'unit_price', 'price_with_tax', 'collection']
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    def calculate_tax(self, product: Product):
        return product.unit_price  * Decimal(1.1)


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']
    products_count =serializers.IntegerField(read_only=True)

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']

    def create(self, validated_data):
        print("test:", validated_data)  # Debugging line
        product_id = self.context['product_id'] # from views.py -> get_serializer_context
        return Review.objects.create(product_id=product_id, **validated_data)

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']

class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer() # No need "many=True" because each CartItem has only one Product
    total_price = serializers.SerializerMethodField()

    # naming convention get_<field_name>
    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price

    class Meta:
        model = CartItem
        fields = ['id','product', 'quantity', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True) # Cart has many CartItems
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart: Cart):
        return sum(item.quantity * item.product.unit_price for item in cart.items.all())

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price'] # here specify the fields that you want to include in the API response sent to the client.

class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    # if we add product that doesn't exist show error
    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('This product does not exist.')
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id'] # передаем через URL
        product_id = self.validated_data['product_id'] # передаются в теле запроса от клиента
        quantity = self.validated_data['quantity'] # передаются в теле запроса от клиента

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item # that's how ModelSerializer->save method works under the hood
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data) # **self.validated_data this is cart_id and prod_id

        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']

class UpdateCartItemSerializer(serializers.ModelSerializer):
    # Prod_id no need because of URL /store/carts/c217eccc-aa3b-4acf-b2bc-dd521ec15c05/items/13/

    class Meta:
        model = CartItem
        fields = ['quantity']


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True) # read_only чтобы избежать ошибки с изменением id

    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership'] # took fields from Customer model

class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'unit_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id', 'customer', 'placed_at', 'payment_status', 'items']

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']

class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('This cart does not exist.')
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError('The cart is empty.')
        return cart_id

    def save(self, **kwargs):
        # Используем transaction.atomic(), чтобы все изменения были либо применены, либо отменены при ошибке
        with transaction.atomic():
            cart_id = self.validated_data['cart_id'] # Получаем cart_id из входных данных

            # Получаем или создаем объект Customer, связанный с текущим пользователем
            customer = Customer.objects.get(user_id=self.context['user_id'])

            # Создаем новый заказ (Order) для этого клиента
            order = Order.objects.create(customer=customer)

            # Получаем все товары из корзины (CartItem), которые относятся к данному cart_id
            cart_items = CartItem.objects \
                        .select_related('product') \
                        .filter(cart_id=cart_id)

            # Преобразуем cart_items в order_items для создания записей в OrderItem
            order_items = [
                OrderItem(order=order,
                       product=item.product,
                       unit_price=item.product.unit_price,
                       quantity=item.quantity
                ) for item in cart_items
            ]

            # Массово создаем все OrderItem записи (быстрее, чем делать .save() для каждого)
            OrderItem.objects.bulk_create(order_items)

            # Удаляем корзину, так как заказ уже оформлен
            Cart.objects.filter(pk=cart_id).delete()

            order_created.send_robust(self.__class__, order=order)

            return order