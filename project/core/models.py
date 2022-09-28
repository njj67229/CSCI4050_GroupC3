from datetime import datetime, timedelta
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
    pic = models.ImageField(blank=True, null=True, upload_to='images/')
    trailer_url = models.URLField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Movies"
    
    def __str__(self):
        return f"{self.title}"

class Promo(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=6)
    discount = models.DecimalField(decimal_places=2, max_digits=3, default=0.1)
    exp_date = models.DateField(default= datetime.now()+ timedelta(days=30))

class Showing(models.Model):
    movie = models.ForeignKey(Movie, on_delete = models.CASCADE)
    showtime = models.DateTimeField()
    room = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.movie} - {self.showtime}"

