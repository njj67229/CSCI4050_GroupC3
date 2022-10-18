from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser
from localflavor.us.models import USStateField
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField
from encrypted_model_fields.fields import EncryptedCharField

# Create your models here.
class CustomerSatus(models.Model):
    status = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name_plural = "Customer Status"
    
    def __str__(self):
        return f"{self.status}, {self.pk}"
    
class Address(models.Model):
    address1 = models.CharField(verbose_name= ('Address line 1'), max_length=1024, default="")
    address2 = models.CharField(verbose_name= ('Address line 2'), max_length=1024, blank=True, null=True )
    city = models.CharField(verbose_name= ('City'), max_length=1024, default='')
    state = USStateField(verbose_name= ('State'), max_length=2, default='' )
    zip_code = models.CharField(verbose_name= ('Postal Code'), max_length=12, default='' )
    # country = models.CharField(verbose_name= ('Country'), max_length=1024, blank=True, null=True )
    
    class Meta:
        verbose_name_plural = "Address"

class PaymentCard(models.Model):
    name = models.CharField(max_length=120, default='',verbose_name= ('Name on Card'))
    # cc_number = CardNumberField(('card number'))
    cc_number = EncryptedCharField(max_length=16, verbose_name= ('Card Number'), primary_key=True)
    cc_expiry = CardExpiryField(('Expiration Date'))
    cc_code = SecurityCodeField(('Security Code'))
    
    
class CustomUser(AbstractUser):
    receive_promos = models.BooleanField(default=False, blank=True, null=True)
    address = models.ForeignKey(Address, on_delete = models.CASCADE, null=True, blank=True)
    # paymentcards = models.ManyToManyField(PaymentCard, blank=True, symmetrical = False)
    status = models.ForeignKey(CustomerSatus, default=2, on_delete=models.PROTECT)
    
    class Meta(AbstractUser.Meta):
       swappable = 'AUTH_USER_MODEL'
       
    def __str__(self):
        return self.username


