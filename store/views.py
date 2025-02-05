from itertools import product

from django.db.models.aggregates import Count
from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView

from store.models import Product, Collection, OrderItem
from rest_framework.response import Response
from rest_framework.decorators import api_view
from store.serializers import ProductSerializer, CollectionSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response(
                {'error': "Product cannot be deleted because it associated with an order item."},
                status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)



class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def delete(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.products.count() > 0:
            return Response(
                {'error': "Collection cannot be deleted because it includes one or more products."},
                status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

