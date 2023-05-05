from django.contrib import admin
from .models import Reservation, Time, Room

# Register your models here.
admin.site.register(Reservation)
admin.site.register(Time)
admin.site.register(Room)