from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.decorators import action
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .filters import (InStockFilterBackend, OrderFilter, ProductFilter,
                      ProductFilter2)
from .models import Order, Product
from .serializers import (OrderSerializer, PorductInfoSerializer,
                          ProductSerializer)

# Create your views here.

# Function-based View to list all products
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)

    return Response(serializer.data)



# Function-based view to show a product details 
@api_view(['GET'])
def product_details(request, pk):
    product = get_object_or_404(Product, pk=pk) 
    serializer = ProductSerializer(product, many=False)

    return Response(serializer.data)



# Function-based View to list all orders
@api_view(['GET'])
def order_list(request):
    # orders = Order.objects.all()
    orders = Order.objects.prefetch_related('items', 'product').all()
    serializer = OrderSerializer(orders, many=True)

    return Response(serializer.data)



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



# Class-based View to list all products
class ProductListAPIView(generics.ListAPIView):
    # queryset = Product.objects.all()
    queryset = Product.objects.filter(stock__gt=10)
    serializer_class = ProductSerializer



# Create a product
class ProductCreateAPIView(generics.CreateAPIView):
    model = Product
    serializer_class = ProductSerializer



# Create and list all products
class ProductListCreateAPIView(generics.ListCreateAPIView):
    # queryset = Product.objects.all()
    queryset = Product.objects.order_by('pk')
    serializer_class = ProductSerializer
    # filterset_fields = ['name', 'price']
    # filterset_class = ProductFilter
    filterset_class = ProductFilter2
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, InStockFilterBackend]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'stock']
    pagination_class = PageNumberPagination
    pagination_class.page_size = 2
    pagination_class.page_query_param = 'pgnum'
    pagination_class .page_size_query_param = 'pgsize'
    
    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()



# Class-based view to show a product details 
class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer



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



class OrderViewSet(ModelViewSet):
    queryset = Order.objects.prefetch_related('items', 'product').all()
    serializer_class = OrderSerializer
    permission_classes=[IsAuthenticated]
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]
    pagination_class = None

    @action(detail=False, methods=['get'], url_path='user-orders')
    def user_orders(self, request):
        orders = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(orders, many=True)
        return Response(serializer.data)