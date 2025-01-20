from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Max
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Order
from .serializers import PorductInfoSerializer, ProductSerializer, OrderSerializer


# Create your views here.

# # List all products
# @api_view(['GET'])
# def product_list(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)

#     return Response(serializer.data)

class ProductListAPIView(generics.ListAPIView):
    # queryset = Product.objects.all()
    queryset = Product.objects.filter(stock__gt=10)
    serializer_class = ProductSerializer


# # Show a product details 
# @api_view(['GET'])
# def product_details(request, pk):
#     product = get_object_or_404(Product, pk=pk) 
#     serializer = ProductSerializer(product, many=False)

#     return Response(serializer.data)

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# # List all orders
# @api_view(['GET'])
# def order_list(request):
#     # orders = Order.objects.all()
#     orders = Order.objects.prefetch_related('items', 'product').all()
#     serializer = OrderSerializer(orders, many=True)

#     return Response(serializer.data)
class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items', 'product').all()
    serializer_class = OrderSerializer


# get all product info
@api_view(['GET'])
def product_info(request):
    products = Product.objects.all()
    max_price = products.aggregate(max_price=Max('price'))['max_price']
    serializer = PorductInfoSerializer({
        'products': products,
        'count': len(products),
        'max_price': max_price
    })

    return Response(serializer.data)
