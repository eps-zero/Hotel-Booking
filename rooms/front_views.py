from django.shortcuts import render, redirect
from .views import (
    RoomListView,
    ReservationListView,
    ReservationCreateView,
    ReservationDetailView,
)
from .serializers import RoomSerializer, ReservationSerializer
from .models import Room


class FrontRoomListView(RoomListView):
    def get(self, request):
        queryset = self.get_queryset()
        serializer = RoomSerializer(queryset, many=True)
        data = serializer.data

        return render(request, "roomList.html", {"rooms": data})


class FrontReservationListView(ReservationListView):
    def get(self, request):
        queryset = self.get_queryset()
        serializer = ReservationSerializer(queryset, many=True)
        data = serializer.data
        return render(request, "reservationList.html", {"reservations": data})


class FrontReservationCreateView(ReservationCreateView):
    def post(self, request):
        response = super().post(request)
        reservation = response.data

        if response.status_code == 201:
            return redirect("front-room-list")
        else:
            rooms = Room.objects.all()
            return render(
                request,
                "reservationCreate.html",
                {"rooms": rooms, "error_message": "Ошибка при создании бронирования."},
            )

    def get(self, request):
        rooms = Room.objects.all()
        return render(request, "reservationCreate.html", {"rooms": rooms})


class FrontReservationDetailView(ReservationDetailView):
    def post(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 200:
            return redirect("front-reservation-list")
