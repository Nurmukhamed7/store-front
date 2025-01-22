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
    queryset = TaggedItem.objects.get_tags_for(Product, 1)

    return render(request, 'hello.html', {'name': "Alex", 'tags': list(queryset)})
