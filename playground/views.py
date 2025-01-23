from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models import F,Q,Value, Func,Count, ExpressionWrapper,DecimalField
from django.db.models.aggregates import Min, Sum
from django.db.models.functions import Concat
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, Customer, Collection, Order, OrderItem, Cart, CartItem
from tags.models import TaggedItem


# Create your views here.
def say_hello(request):
    queryset = Product.objects.raw('SELECT * FROM store_product')


    return render(request, 'hello.html', {'name': "Alex", 'result': list(queryset)})
