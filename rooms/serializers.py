from rest_framework import serializers
from .models import Room, Reservation
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"], password=validated_data["password"]
        )
        return user


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "room_number", "price_per_day", "capacity"]


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["id", "user", "room",
                  "start_booking_date", "end_booking_date"]

    def create(self, validated_data):
        room_id = validated_data["room"].id
        start_booking_date = validated_data["start_booking_date"]
        end_booking_date = validated_data["end_booking_date"]

        existing_reservation = Reservation.objects.filter(
            room_id=room_id,
            start_booking_date__lte=end_booking_date,
            end_booking_date__gte=start_booking_date,
        ).exists()

        if start_booking_date > end_booking_date:
            raise serializers.ValidationError(
                "Check in date should be earlier that check out date."
            )

        if existing_reservation:
            raise serializers.ValidationError(
                "This room is already booked for the selected time period."
            )

        reservation = Reservation.objects.create(**validated_data)

        return reservation
