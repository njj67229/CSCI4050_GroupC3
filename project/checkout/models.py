import datetime
from django.db import models
from django.conf import settings
import string
import random
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from core.models import Showing, Promo
from accounts.models import CustomUser

class TicketType(models.Model):
    class TicketType(models.TextChoices):
        ADULT = "AD", _("ADULT")
        CHILD = "CH", _("CHILD")
        SENIOR = "SR", _("SENIOR")
    
    type = models.CharField(max_length=2, choices=TicketType.choices, default=TicketType.ADULT)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=4)
   
    def __str__(self):
        return f"{self.type}-{self.price}"
    
class Ticket(models.Model):
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE, default="")
    showing = models.ForeignKey("core.Showing", on_delete=models.CASCADE)
    # seat = models.ForeignKey("core.SeatInShowing", on_delete=models.PROTECT)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=4)

    def __str__(self):
        return f"{self.id}"

class TicketFactory:
    """
    Class that builds and returns ticket object and updates proce based on selected option

    Returns:
        Ticket object with correct pricing information
    """
    def __init__(self, type='AD', showing_id = 1,):
        #need to create a ticket for that showing, with correct price 
        s = Showing.objects.get(pk=showing_id) #particular showing
        t_type = TicketType.objects.get(type=type) #how to get based on choice
        
        self.ticket = Ticket(ticket_type=t_type, showing=s, price=t_type.price)
    
    def get_ticket(self):
        """
        Returns a ticket object associated with the correct ticket type object
        """
        return self.ticket


class Booking(models.Model):
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    promo = models.ForeignKey(
        "core.Promo", blank=True, null=True, on_delete=models.PROTECT
    )
    showing = models.ForeignKey("core.Showing", on_delete=models.CASCADE)
    tickets = models.ManyToManyField(Ticket)
    
    def caclculate_price(self):
        price = 0
        for t in self.tickets.all():
            price += t.price

        if self.promo:
            #apply promo here
            if self.promo.exp_date >= datetime.datetime.now().date():
                #if promo is still valid
                return (1-self.promo.discount)*price
        
        return price
    
    

    
            

    def __str__(self):
        return f"{self.id}"


# Create your models here.

