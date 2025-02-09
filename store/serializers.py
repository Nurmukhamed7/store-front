from rest_framework import serializers
from decimal import Decimal
from store.models import Product, Collection, Review, Cart, CartItem


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title']


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
