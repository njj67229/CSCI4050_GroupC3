from pydoc import synopsis
from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=200)
    tag_line = models.TextField(blank=True, null=True)
    rating = models.CharField(max_length=200)
    runtime = models.IntegerField(blank=True, null=True)
    release_date = models.DateField(null=True)
    synopsis = models.TextField(blank=True, null=True)
    pic = models.ImageField(blank=True, null=True)
    trailer_url = models.URLField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Movies"
    
    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

class Promo(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=6)
