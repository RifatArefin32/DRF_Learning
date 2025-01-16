from django.urls import path
from .views import product_list, product_details, order_list

urlpatterns = [
    path('products/', product_list, name='product_list'),
    path('products/<int:pk>/', product_details, name='product_details'),
    path('orders/', order_list, name='order_list'),
]
