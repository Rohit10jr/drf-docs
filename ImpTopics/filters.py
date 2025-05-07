# filters.py
import django_filters
from .models import Product
from rest_framework import filters

class ProductFilter(django_filters.FilterSet):
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    category = django_filters.CharFilter(field_name='category', lookup_expr='iexact')
    in_stock = django_filters.BooleanFilter(field_name='in_stock')

    class Meta:
        model = Product
        fields = ['category', 'min_price', 'max_price', 'in_stock']


class CustomSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        if request.query_params.get('username_only'):
            return ['username']
        return super().get_search_fields(view, request)