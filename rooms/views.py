import datetime
from rest_framework import generics, permissions
from .models import Room, Reservation
from .serializers import UserSerializer, RoomSerializer, ReservationSerializer
from rest_framework.response import Response
from .filters import RoomFilter
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework import status


class RoomListView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        queryset = Room.objects.all()
        room_filter = RoomFilter(self.request.GET, queryset=queryset)
        filtered_queryset = room_filter.qs

        params = self.request.GET

        check_in_date = params.get("check_in_date")
        check_out_date = params.get("check_out_date")

        filter_kwargs = {}

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
                    "Invalid date format. Please use YYYY-MM-DD format.")

            # Выполняем фильтрацию комнат
            reserved_rooms_start = Reservation.objects.filter(
                start_booking_date__lte=check_out_date,
                start_booking_date__gte=check_in_date,
            ).values_list("room", flat=True)
            reserved_rooms_end = Reservation.objects.filter(
                end_booking_date__gte=check_in_date,
                end_booking_date__lte=check_out_date,
            ).values_list("room", flat=True)
            reserved_rooms = set(reserved_rooms_start) | set(
                reserved_rooms_end)
            filtered_queryset = filtered_queryset.exclude(
                id__in=reserved_rooms)

            if check_in_date > check_out_date:
                raise ValueError(
                    "Check in date should be earlier that check out date.")

        return filtered_queryset

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


class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        user = serializer.instance
        response_data = {
            "user": UserSerializer(user).data,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
