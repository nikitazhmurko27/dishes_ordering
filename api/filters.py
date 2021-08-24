from django_filters import rest_framework as filters
from dishes.models import Dish


class DishesFilter(filters.FilterSet):
    date_from = filters.DateFilter(field_name='created_at', lookup_expr='gte')
    date_to = filters.DateFilter(field_name="created_at", lookup_expr='lte')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Dish
        fields = ['name', 'date_from', 'date_to']
