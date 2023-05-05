from django.db import models

# Create your models here.


class Reservation(models.Model):
    date = models.DateField(auto_created=False)
    time = models.CharField(max_length=5)
    room = models.CharField(max_length=25, null=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.time} + {self.date}"


class Time(models.Model):
    time_slot = models.CharField(max_length=5)

    class Meta:
        ordering = ['time_slot']

    def __str__(self):
        return f"{self.time_slot}"


class Room(models.Model):
    room = models.CharField(max_length=25)

    class Meta:
        ordering = ['room']

    def __str__(self):
        return f"{self.room}"