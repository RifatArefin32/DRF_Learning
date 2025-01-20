from django.urls import path
from .views import product_list, product_details, order_list, product_info

urlpatterns = [
    path('products/', product_list, name='product_list'),
    path('products/info/', product_info, name='product_info'),
    path('products/<int:pk>/', product_details, name='product_details'),
    path('orders/', order_list, name='order_list'),
]
