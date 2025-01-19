from django.db.models import F,Q
from django.db.models.aggregates import Count, Min, Sum
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, Customer, Collection, Order, OrderItem


# Create your views here.
def say_hello(request):
    # result = Product.objects.aggregate(count = Count('id'), min_price=Min('unit_price'))

    result = OrderItem.objects.filter(product__id=1).aggregate(units_sold=Sum('quantity'))


    return render(request, 'hello.html', {'name': "Alex", 'result': result})
