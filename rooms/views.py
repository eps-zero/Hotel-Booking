import datetime
from rest_framework import generics, permissions
from .models import Room, Reservation
from .serializers import RoomSerializer, ReservationSerializer
from rest_framework.response import Response


class RoomListView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        params = self.request.GET

        min_price = params.get("min_price")
        max_price = params.get("max_price")
        capacity = params.get("capacity")
        ordering = params.get("ordering")
        check_in_date = params.get("check_in_date")
        check_out_date = params.get("check_out_date")

        queryset = Room.objects.all()
        filter_kwargs = {}

        if params:
            if min_price:
                queryset = queryset.filter(price_per_day__gte=min_price)

            if max_price:
                queryset = queryset.filter(price_per_day__lte=max_price)

            if capacity:
                queryset = queryset.filter(capacity=capacity)

            if ordering == "price":
                queryset = queryset.order_by("price_per_day")
            elif ordering == "-price":
                queryset = queryset.order_by("-price_per_day")
            elif ordering == "capacity":
                queryset = queryset.order_by("capacity")
            elif ordering == "-capacity":
                queryset = queryset.order_by("-capacity")

            if check_in_date and check_out_date:
                try:
                    check_in_date = datetime.datetime.strptime(
                        check_in_date, "%Y-%m-%d"
                    ).date()
                    check_out_date = datetime.datetime.strptime(
                        check_out_date, "%Y-%m-%d"
                    ).date()
                except ValueError:
                    raise ValueError(
                        "Invalid date format. Please use YYYY-MM-DD format."
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

                if check_in_date > check_out_date:
                    raise ValueError(
                        "Check in date should be earlier that check out date."
                    )

        return queryset

    def get(self, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = RoomSerializer(queryset, many=True)
            return Response(serializer.data)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)


class ReservationListView(generics.ListAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Reservation.objects.filter(user=self.request.user.id)
        return queryset


class ReservationCreateView(generics.CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ReservationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        reservation_id = kwargs["pk"]
        try:
            reservation = Reservation.objects.get(id=reservation_id)
            reservation.delete()
            return Response({"message": "Reservation cancelled successfully."})
        except Reservation.DoesNotExist:
            return Response({"error": "Reservation not found."})
