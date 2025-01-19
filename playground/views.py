from django.db.models import F,Q
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, Customer, Collection, Order, OrderItem


# Create your views here.
def say_hello(request):
    # query_set = Product.objects.prefetch_related('promotion').select_related('collection').all()

    # Get last 5 orders with their customer and items (incl product)
    query_set = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]

    return render(request, 'hello.html', {'name': "Alex", 'orders': list(query_set)})
