from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Room, Reservation


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "room_number", "name", "price_per_day", "capacity"]

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["id", "user", "room", "start_booking_date", "end_booking_date"]

    def create(self, validated_data):
        room_id = validated_data["room"].id
        start_booking_date = validated_data["start_booking_date"]
        end_booking_date = validated_data["end_booking_date"]

        existing_reservation = Reservation.objects.filter(
            room_id=room_id,
            start_booking_date__lte=end_booking_date,
            end_booking_date__gte=start_booking_date,
        ).exists()

        if existing_reservation:
            raise serializers.ValidationError(
                "This room is already booked for the selected time period."
            )

        reservation = Reservation.objects.create(**validated_data)

        return reservation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}
