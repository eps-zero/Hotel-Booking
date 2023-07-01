from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient

from .models import Room


class RoomTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.superuser = User.objects.create_superuser(
            username="superuseer", password="mikeTyson"
        )
        self.room = Room.objects.create(
            room_number="101",
            name="Fifth floar terrace room",
            price_per_day=100.00,
            capacity=2,
        )

    def test_add_room(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(
            reverse("room-create"),
            {
                "room_number": "144",
                "name": "Fifth floar terrace room",
                "price_per_day": 140.00,
                "capacity": 3,
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Room.objects.count(), 2)

    def test_delete_room(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(reverse("room-detail", args=[self.room.pk]))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Room.objects.count(), 0)
