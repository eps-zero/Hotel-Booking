import datetime
from rest_framework import generics, permissions
from .models import Room, Reservation
from .serializers import RoomSerializer, ReservationSerializer, UserSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, redirect


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

            if check_in_date:
                try:
                    check_in_date = datetime.datetime.strptime(
                        check_in_date, "%Y-%m-%d"
                    ).date()
                    filter_kwargs["end_booking_date__gte"] = check_in_date
                except ValueError:
                    raise ValueError(
                        "Invalid check-in date format. Please use YYYY-MM-DD format."
                    )

            if check_out_date:
                try:
                    check_out_date = datetime.datetime.strptime(
                        check_out_date, "%Y-%m-%d"
                    ).date()
                    filter_kwargs["start_booking_date__lte"] = check_out_date
                except ValueError:
                    raise ValueError(
                        "Invalid check-out date format. Please use YYYY-MM-DD format."
                    )

                if check_in_date:
                    if check_in_date > check_out_date:
                        raise ValueError("Check-in date must be before check-out date.")

            reserved_rooms = Reservation.objects.filter(**filter_kwargs).values_list(
                "room_id", flat=True
            )

            queryset = queryset.exclude(id__in=reserved_rooms)

        return queryset

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = RoomSerializer(queryset, many=True)
            return Response(serializer.data)

        except ValueError as e:
            return Response({"error": str(e)}, status=400)


class RoomCreateView(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (permissions.IsAdminUser,)


class ReservationListView(generics.ListAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = (permissions.IsAuthenticated,)


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


class UserSignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class UserLoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "Invalidü credentials"})

        if user.password == password:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return Response({"error": "Invalide credentials"})
