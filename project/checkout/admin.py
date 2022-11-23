from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Ticket, Booking, ChildTicket, AdultTicket, SeniorTicket

# Register your models here.


# @admin.register(Ticket)
# class TicketAdmin(admin.ModelAdmin):
#     pass

@admin.register(ChildTicket)
class ChildTicketAdmin(admin.ModelAdmin):
    pass

@admin.register(AdultTicket)
class AdultTicketAdmin(admin.ModelAdmin):
    pass

@admin.register(SeniorTicket)
class SeniorTicketAdmin(admin.ModelAdmin):
    pass

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    pass
