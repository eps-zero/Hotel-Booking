from django_filters import rest_framework as filters
from .models import Room


class RoomFilter(filters.FilterSet):
    min_price = filters.NumberFilter(
        field_name="price_per_day", lookup_expr="gte")
    max_price = filters.NumberFilter(
        field_name="price_per_day", lookup_expr="lte")
    capacity = filters.NumberFilter()

    ordering = filters.OrderingFilter(
        fields=(
            ("capacity", "capacity"),
            ("price_per_day", "price"),
        )
    )

    class Meta:
        model = Room
        fields = ["min_price", "max_price", "capacity"]
