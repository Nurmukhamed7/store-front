from django.contrib.contenttypes.models import ContentType
from django.db.models import F,Q,Value, Func,Count, ExpressionWrapper,DecimalField
from django.db.models.aggregates import Min, Sum
from django.db.models.functions import Concat
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, Customer, Collection, Order, OrderItem
from tags.models import TaggedItem


# Create your views here.
def say_hello(request):
    # collection = Collection.objects.get(pk=11)
    # collection.featured_product = None
    # collection.save()

    Collection.objects.filter(pk=11).update(featured_product=None)

    return render(request, 'hello.html', {'name': "Alex"})
