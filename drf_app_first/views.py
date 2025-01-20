from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Max
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product, Order
from .serializers import PorductInfoSerializer, ProductSerializer, OrderSerializer


# Create your views here.



# Function-based View to list all products
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)

    return Response(serializer.data)



# Class-based View to list all products
class ProductListAPIView(generics.ListAPIView):
    # queryset = Product.objects.all()
    queryset = Product.objects.filter(stock__gt=10)
    serializer_class = ProductSerializer



# Function-based view to show a product details 
@api_view(['GET'])
def product_details(request, pk):
    product = get_object_or_404(Product, pk=pk) 
    serializer = ProductSerializer(product, many=False)

    return Response(serializer.data)



# Class-based view to show a product details 
class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer



# Function-based View to list all orders
@api_view(['GET'])
def order_list(request):
    # orders = Order.objects.all()
    orders = Order.objects.prefetch_related('items', 'product').all()
    serializer = OrderSerializer(orders, many=True)

    return Response(serializer.data)



# Class-based View to list all products
class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items', 'product').all()
    serializer_class = OrderSerializer



# Class-based View to list all orders of current user
class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items', 'product').all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        return qs.filter(user=user)



# Function-based View to list all product info
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



# Class-based View to list all product info
class ProductInfoAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        max_price = products.aggregate(max_price=Max('price'))['max_price']
        serializer = PorductInfoSerializer({
            'products': products,
            'count': len(products),
            'max_price': max_price
        })

        return Response(serializer.data)
