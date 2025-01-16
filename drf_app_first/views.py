from django.http import JsonResponse
from .models import Product
from .serializers import ProductSerializer

# Create your views here.
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)

    return JsonResponse({
        "data": serializer.data
    })