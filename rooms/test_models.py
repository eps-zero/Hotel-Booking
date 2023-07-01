from django.test import TestCase
from rooms.models import Room, Reservation
from django.contrib.auth.models import User
from datetime import date


class RoomModelTest(TestCase):
    def setUp(self):
        self.room = Room.objects.create(
            room_number="101",
            name="Fifth floar terrace room",
            price_per_day=100.00,
            capacity=2,
        )

    def test_room_fields(self):
        self.assertEqual(self.room.room_number, "101")
        self.assertEqual(self.room.name, "Fifth floar terrace room")
        self.assertEqual(self.room.price_per_day, 100.00)
        self.assertEqual(self.room.capacity, 2)


class ReservationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="admin", password="mikeTyson")
        self.room = Room.objects.create(
            room_number="101",
            name="Fifth floar terrace room",
            price_per_day=100.00,
            capacity=2,
        )
        self.reservation = Reservation.objects.create(
            room=self.room,
            user=self.user,
            start_booking_date=date.today(),
            end_booking_date=date.today(),
        )

    def test_reservation_fields(self):
        self.assertEqual(self.reservation.room, self.room)
        self.assertEqual(self.reservation.user, self.user)
        self.assertEqual(self.reservation.start_booking_date, date.today())
        self.assertEqual(self.reservation.end_booking_date, date.today())
