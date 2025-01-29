import django_filters
from rest_framework import filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['name', 'price']


class ProductFilter2(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'name':['exact', 'contains'], 
            'price':['exact', 'lt', 'gt', 'range']
        }


class InStockFilterBackend(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(stock__gt=10)