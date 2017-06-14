from django.contrib import admin

# Register your models here.
from .models import Reservation, Auditorium


admin.site.register(Reservation)
admin.site.register(Auditorium)
