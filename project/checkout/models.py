from datetime import datetime, timedelta
from django.db import models
from django.conf import settings
import string
import random
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _


class Ticket(models.Model):
    class TicketType(models.TextChoices):
        ADULT = "AD", _("ADULT")
        CHILD = "CH", _("CHILD")
        SENIOR = "SR", _("SENIOR")

    ticket_id = models.IntegerField(primary_key=True, unique=True)
    ticket_type = models.CharField(max_length=2, choices=TicketType.choices)
    showing = models.ForeignKey("core.Showing", on_delete=models.CASCADE)
    seat = models.ForeignKey("core.SeatInShowing", null=True, on_delete=models.PROTECT, related_name="ticket_seat")

    def __str__(self):
        return f"{self.ticket_id}"


class Booking(models.Model):
    booking_id = models.IntegerField(primary_key=True, unique=True)
    promo = models.ForeignKey(
        "core.Promo", blank=True, null=True, on_delete=models.PROTECT
    )
    showing = models.ForeignKey("core.Showing", on_delete=models.CASCADE)
    tickets = models.ManyToManyField(Ticket)
    user = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE)
    card_id = models.ForeignKey("accounts.PaymentCard", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.booking_id}"


# Create your models here.
