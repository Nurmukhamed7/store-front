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
    # ... some code here

    with transaction.atomic():
        # parent record
        order=Order()
        order.customer_id = 1
        order.save()

        # child record
        item = OrderItem()
        item.order = order
        item.product_id = -1
        item.quantity = 1
        item.unit_price = 10
        item.save()

    return render(request, 'hello.html', {'name': "Alex"})
