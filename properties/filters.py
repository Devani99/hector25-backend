import django_filters
from .models import Property


class PropertyFilter(django_filters.FilterSet):
    """Filter properties by type, listing_type, price range, bedrooms, and location."""
    type = django_filters.CharFilter(field_name='type', lookup_expr='iexact')
    listing_type = django_filters.CharFilter(field_name='listing_type', lookup_expr='iexact')
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    bedrooms = django_filters.NumberFilter(field_name='bedrooms')
    bedrooms_min = django_filters.NumberFilter(field_name='bedrooms', lookup_expr='gte')
    location = django_filters.CharFilter(field_name='location', lookup_expr='icontains')
    featured = django_filters.BooleanFilter(field_name='is_featured')

    class Meta:
        model = Property
        fields = ['type', 'listing_type', 'price_min', 'price_max', 'bedrooms', 'location']
