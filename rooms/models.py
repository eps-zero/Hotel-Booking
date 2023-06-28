from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    room_number = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.room_number

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_booking_date = models.DateField()
    end_booking_sate = models.DateField()
    
    def __str__(self):
        return f"Reservation {self.id} - {self.room.room_number}"