from django.contrib import admin
from .models import Reservation, Time, Room, TestModel

# Register your models here.
admin.site.register(Reservation)
admin.site.register(Time)
admin.site.register(Room)
admin.site.register(TestModel)