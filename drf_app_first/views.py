from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer


# Create your views here.

# List all products
@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)

    return Response(serializer.data)



# Show a product details 
@api_view(['GET'])
def product_details(request, pk):
    product = get_object_or_404(Product, pk=pk) 
    serializer = ProductSerializer(product, many=False)

    return Response(serializer.data)



# List all orders
@api_view(['GET'])
def order_list(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)

    return Response(serializer.data)
