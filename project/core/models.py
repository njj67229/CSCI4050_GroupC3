from datetime import datetime, timedelta
from pydoc import synopsis
from django.db import models
import string
import random

def get_code(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
    
# Create your models here.
class Genre(models.Model):
    
    title = models.CharField(max_length=200, unique=True)
    
    def __str__(self):
        return f"{self.title, self.pk}"

class MPAA(models.Model):
    
    rating = models.CharField(max_length=200, unique=True)
    
    class Meta:
        verbose_name_plural = "MPAA Rating"
    
    def __str__(self):
        return f"{self.rating, self.pk}"
    
class Movie(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    title = models.CharField(max_length=200)
    tag = models.TextField(blank=True, null=True)
    rating = models.CharField(max_length=200)
    runtime = models.CharField(max_length=200, null=True)
    release_date = models.DateField(null=True)
    synopsis = models.TextField(blank=True, null=True)
    pic = models.ImageField(blank=True, null=True, upload_to='images/')
    trailer_url = models.URLField(blank=True, null=True)
    producer = models.CharField(max_length=200, blank=True, null=True)
    director = models.CharField(max_length=200, blank=True, null=True)
    genres = models.ManyToManyField(Genre)
    
    class Meta:
        verbose_name_plural = "Movies"
    
    def __str__(self):
        return f"{self.title}"

class Promo(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=6, default=get_code())
    discount = models.DecimalField(decimal_places=2, max_digits=3, default=0.1)
    exp_date = models.DateField(default= datetime.now()+ timedelta(days=30))
    
    def __str__(self):
        return f"{self.name}"
    

class Showing(models.Model):
    movie = models.ForeignKey(Movie, on_delete = models.CASCADE)
    showtime = models.DateTimeField()
    room = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.movie} - {self.showtime}"

    

