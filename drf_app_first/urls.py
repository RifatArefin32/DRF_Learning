from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProductDetailAPIView, OrderListAPIView, UserOrderListAPIView, ProductInfoAPIView, ProductListCreateAPIView, OrderViewSet

urlpatterns = [
    # path('products/', product_list, name='product_list'),
    # path('products/info/', product_info, name='product_info'),
    # path('products/<int:pk>/', product_details, name='product_details'),
    # path('orders/', order_list, name='order_list'),
    # path('products/create/', ProductCreateAPIView.as_view(), name='product_create'),
    # path('products/', ProductListAPIView.as_view(), name='product_list'),
    
    path('products/', ProductListCreateAPIView.as_view(), name='product_list'),
    path('products/info/', ProductInfoAPIView.as_view(), name='product_info'),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='product_details'),
    # path('orders/', OrderListAPIView.as_view(), name='order_list'),
    # path('user-orders/', UserOrderListAPIView.as_view(), name='user_order_list'),
]

routers = DefaultRouter()
routers.register('orders', OrderViewSet)

urlpatterns += routers.urls