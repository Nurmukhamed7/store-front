from django.db.models import F,Q
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, Customer, Collection, Order, OrderItem


# Create your views here.
def say_hello(request):
    # select products that has been ordered and sort by title
    # filter product by looking up in OrderItem
    # go to product table and select all with query_set id above:
    query_set = Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')

    return render(request, 'hello.html', {'name': "Alex", 'products': list(query_set)})
