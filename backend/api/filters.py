# filters.py
import django_filters
from .models import Service

class ServiceFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    location = django_filters.CharFilter(field_name='provider__location', lookup_expr='icontains')
    skill = django_filters.CharFilter(method='filter_by_skill')

    class Meta:
        model = Service
        fields = ['service_type', 'payment_type']

    def filter_by_skill(self, queryset, name, value):
        return queryset.filter(skills__name__icontains=value).distinct() 
