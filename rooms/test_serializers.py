from django.test import TestCase
from .models import Room, Reservation
from .serializers import RoomSerializer, ReservationSerializer
from django.contrib.auth.models import User
from datetime import date


class RoomSerializerTest(TestCase):
    def setUp(self):
        self.room = Room.objects.create(
            room_number='101',
            name='Fifth floar terrace room',
            price_per_day=100.00,
            capacity=2
        )
        self.serializer = RoomSerializer(instance=self.room)

    def test_room_serializer_fields(self):
        data = self.serializer.data
        self.assertEqual(data['room_number'], '101')
        self.assertEqual(data['name'], 'Fifth floar terrace room')
        self.assertEqual(data['price_per_day'], '100.00')
        self.assertEqual(data['capacity'], 2)


class ReservationSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='admin', password='mikeTyson')
        self.room = Room.objects.create(
            room_number='101',
            name='Fifth floar terrace room',
            price_per_day=100.00,
            capacity=2
        )
        self.reservation = Reservation.objects.create(
            room=self.room,
            user=self.user,
            start_booking_date=date.today(),
            end_booking_date=date.today()
        )
        self.serializer = ReservationSerializer(instance=self.reservation)

    def test_reservation_serializer_fields(self):
        data = self.serializer.data
        self.assertEqual(data['room'], self.room.id)
        self.assertEqual(data['user'], self.user.id)
        self.assertEqual(data['start_booking_date'], str(date.today()))
        self.assertEqual(data['end_booking_date'], str(date.today()))
