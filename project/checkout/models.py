from datetime import datetime, timedelta
from django.db import models
from django.conf import settings
import string
import random
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from core.models import Showing

class Ticket(models.Model):
    class TicketType(models.TextChoices):
        ADULT = "AD", _("ADULT")
        CHILD = "CH", _("CHILD")
        SENIOR = "SR", _("SENIOR")

    # ticket_type = models.CharField(max_length=2, choices=TicketType.choices)
    showing = models.ForeignKey("core.Showing", on_delete=models.CASCADE, default=4)
    # seat = models.ForeignKey("core.SeatInShowing", on_delete=models.PROTECT)
    # price = models.DecimalField(default=0, decimal_places=2, max_digits=4)

    def __str__(self):
        return f"{self.id}"
    
    class Meta:
        abstract = True
    
class AdultTicket(Ticket):
    price = models.DecimalField(default=10, decimal_places=2, max_digits=4)
    
    def __str__(self):
        return "Adult"

class ChildTicket(Ticket):
    price = models.DecimalField(default=7, decimal_places=2, max_digits=4)
    
    def __str__(self):
        return "Child"

class SeniorTicket(Ticket):
    price = models.DecimalField(default=8, decimal_places=2, max_digits=4)
    
    def __str__(self):
        return "Senior"

class TicketFactory:
    """Class that takes a string val for choice and creats a ticket type object
       Its type field will be of type Child, Adult, or Senior
    """
    def __init__(self, type = 'Adult', showing_id = 4):
        """Ticket factory is our abstract factory"""
        localizers = {
        "Adult": AdultTicket,
        "Child": ChildTicket,
        "Senior": SeniorTicket,
        }
 
        self.type = localizers[type]() #adult object
        s = Showing.objects.get(pk=showing_id)
        self.type.__class__.objects.create(showing=s)
        # self.type.showing = showing_id
 
    # def make_ticket(self):
    #     """creates and shows tickets using the abstract factory"""
 
    #     ticket = self.type()
 
    #     print(f'We have a ticket of type {ticket}')
    #     print(f'its price is {ticket.price}')
    #     return ticket   
    
    def __str__(self):
        return str(self.type) 


class Booking(models.Model):
    
    promo = models.ForeignKey(
        "core.Promo", blank=True, null=True, on_delete=models.PROTECT
    )
    showing = models.ForeignKey("core.Showing", on_delete=models.CASCADE)
    # tickets = models.ManyToManyField(Ticket)
    # tickets = GenericForeignKey()

    def __str__(self):
        return f"{self.id}"


# Create your models here.

