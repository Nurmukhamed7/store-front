from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, Customer, Collection, Order


# Create your views here.
def say_hello(request):
    # Products: inventory < 10 AND price < 20
    query_set = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20)) #OR
    # query_set = Product.objects.filter(Q(inventory__lt=10) & ~Q(unit_price__lt=20)) # ~ means NOT
    # query_set = Product.objects.filter(Q(inventory__lt=10) & ~Q(unit_price__lt=20)) #AND



    return render(request, 'hello.html', {'name': "Alex", 'products': list(query_set)})
