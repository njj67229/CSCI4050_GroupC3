from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Ticket, Booking

# Register your models here.


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    pass
