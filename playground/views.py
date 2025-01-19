from django.db.models import F,Q,Value, Func
from django.db.models.aggregates import Count, Min, Sum
from django.db.models.functions import Concat
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, Customer, Collection, Order, OrderItem


# Create your views here.
def say_hello(request):
    #CONCAT
    # queryset = Customer.objects.annotate(
    #     full_name=Func(F('first_name'), Value(' '), F('last_name'), function='CONCAT')
    # )

    queryset = Customer.objects.annotate(
        full_name=Concat('first_name', Value(' '), 'last_name')
    )

    return render(request, 'hello.html', {'name': "Alex", 'result': list(queryset)})
