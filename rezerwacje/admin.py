from django.contrib import admin

# Register your models here.
from .models import Reservation, Auditorium


class AuditoriumAdmin(admin.ModelAdmin):

    list_display = ('name', 'capacity', 'projector')
    search_fields = ['name']
    list_filter = ['capacity', 'projector', 'reservations__date']


class ReservationAdmin(admin.ModelAdmin):

    list_display = ('auditorium', 'date',)
    search_fields = ['auditorium',]
    list_filter = ['date', 'comment',]

admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Auditorium, AuditoriumAdmin)
