from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Room, Reservation
from django.contrib.auth.models import User
from datetime import date


class RoomViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='admin', password='mikeTyson')
        self.client.force_authenticate(user=self.user)
        self.room = Room.objects.create(
            room_number='101',
            name='Fifth floar terrace room',
            price_per_day=100.00,
            capacity=2
        )

    def test_get_all_rooms(self):
        url = reverse('room-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class ReservationViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='admin', password='mikeTyson')
        self.client.force_authenticate(user=self.user)
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

    def test_get_all_reservations(self):
        url = reverse('reservation-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
