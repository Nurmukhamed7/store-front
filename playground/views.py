from django.db.models import F,Q,Value, Func,Count
from django.db.models.aggregates import Min, Sum
from django.db.models.functions import Concat
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, Customer, Collection, Order, OrderItem


# Create your views here.
def say_hello(request):
    queryset = Customer.objects.annotate(
        orders_count=Count('order'),
    )

    return render(request, 'hello.html', {'name': "Alex", 'result': list(queryset)})
