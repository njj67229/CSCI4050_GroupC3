from threading import local
from django.db import models
from django.contrib.auth.models import AbstractUser
from localflavor.us.models import USStateField
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField


# Create your models here.
class Address(models.Model):
    address1 = models.CharField(verbose_name= ('Address line 1'), max_length=1024, blank=True, null=True )
    address2 = models.CharField(verbose_name= ('Address line 2'), max_length=1024, blank=True, null=True )
    city = models.CharField(verbose_name= ('City'), max_length=1024, blank=True, null=True )
    sate = USStateField(verbose_name= ('State'), max_length=2, blank=True, null=True )
    zip_code = models.CharField(verbose_name= ('Postal Code'), max_length=12, blank=True, null=True )
    # country = models.CharField(verbose_name= ('Country'), max_length=1024, blank=True, null=True )

class PaymentCard(models.Model):
    name = models.CharField(max_length=120, blank=True, null=True)
    cc_number = CardNumberField(('card number'))
    cc_expiry = CardExpiryField(('expiration date'))
    cc_code = SecurityCodeField(('security code'))
    
class CustomUser(AbstractUser):
    receive_promos = models.BooleanField(default=False)
    address = models.ForeignKey(Address, on_delete = models.CASCADE, null=True)
    paymentcards = models.ManyToManyField(PaymentCard)
    
    def __str__(self):
        return self.username


