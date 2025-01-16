from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, Customer, Collection, Order


# Create your views here.
def say_hello(request):
    query_set = Product.objects.filter()
    # query_set = Product.objects.filter(description__isnull=True)
    # query_set = Customer.objects.filter(email__icontains='.com')
    # query_set = Collection.objects.filter(featured_product__isnull=True)
    # query_set = Product.objects.filter(inventory__lt=10)
    # query_set = Order.objects.filter(customer__id=1)
    # query_set = Order.objects.filter(product__collection__id=3)


    return render(request, 'hello.html', {'name': "Alex", 'products': list(query_set)})
