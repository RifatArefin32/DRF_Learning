from django.urls import path
from .views import product_info, ProductListAPIView, ProductDetailAPIView, OrderListAPIView, UserOrderListAPIView

urlpatterns = [
    # path('products/', product_list, name='product_list'),
    path('products/', ProductListAPIView.as_view(), name='product_list'),
    path('products/info/', product_info, name='product_info'),
    # path('products/<int:pk>/', product_details, name='product_details'),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='product_details'),
    # path('orders/', order_list, name='order_list'),
    path('orders/', OrderListAPIView.as_view(), name='order_list'),
    path('user-orders/', UserOrderListAPIView.as_view(), name='user_order_list'),
]
