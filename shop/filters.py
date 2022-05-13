import django_filters
from django_filters import CharFilter, NumberFilter


from .models import Product
class ProductFilter(django_filters.FilterSet):
    name = CharFilter(lookup_expr='icontains')
    max_price=NumberFilter(field_name='price' ,lookup_expr='lte')
    min_price=NumberFilter(field_name='price' ,lookup_expr='gte')

    class Meta:
        model = Product
        fields = ['price', 'categorie']