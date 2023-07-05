from django_filters import rest_framework as filters
from .models import Room, Reservation
from django.core.exceptions import ValidationError


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

    # Всё-таки я придумал что-то такое. Да функция та же,
    # но пользуюсь библиотекой django-filters)))) ну реально я
    # не знаю как именно эту логику устроить через стандартные функции
    date_range = filters.DateFromToRangeFilter(method='date_filter')

    def date_filter(self, queryset, name, value):

        check_in_date = value.start
        check_out_date = value.stop

        if check_in_date > check_out_date:
            raise ValidationError(
                'Check-in date should be earlier than check-out date.'
            )

        # Выполняем фильтрацию комнат
        reserved_rooms_start = Reservation.objects.filter(
            start_booking_date__lte=check_out_date,
            start_booking_date__gte=check_in_date,
        ).values_list("room", flat=True)
        reserved_rooms_end = Reservation.objects.filter(
            end_booking_date__gte=check_in_date,
            end_booking_date__lte=check_out_date,
        ).values_list("room", flat=True)
        reserved_rooms = set(reserved_rooms_start) | set(reserved_rooms_end)
        queryset = queryset.exclude(id__in=reserved_rooms)

        return queryset

    class Meta:
        model = Room
        fields = ["min_price", "max_price", "capacity", "date_range"]
