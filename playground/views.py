from django.db.models import F,Q,Value
from django.db.models.aggregates import Count, Min, Sum
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, Customer, Collection, Order, OrderItem


# Create your views here.
def say_hello(request):
    queryset = Customer.objects.annotate(new_id = F('id'))


    return render(request, 'hello.html', {'name': "Alex", 'result': list(queryset)})
