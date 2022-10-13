from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Address(models.Model):
    address1 = models.CharField(verbose_name= ('Address line 1'), max_length=1024, blank=True, null=True )
    address2 = models.CharField(verbose_name= ('Address line 2'), max_length=1024, blank=True, null=True )
    zip_code = models.CharField(verbose_name= ('Postal Code'), max_length=12, blank=True, null=True )
    city = models.CharField(verbose_name= ('City'), max_length=1024, blank=True, null=True )
    sate = models.CharField(verbose_name= ('State'), max_length=2, blank=True, null=True )
    country = models.CharField(verbose_name= ('Country'), max_length=1024, blank=True, null=True )
    
class CustomUser(AbstractUser):
    receive_promos = models.BooleanField(default=False)
    address = models.ForeignKey(Address, on_delete = models.CASCADE, null=True)
    
    def __str__(self):
        return self.username


