from pydoc import synopsis
from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=200)
    tag_line = models.TextField()
    rating = models.CharField(max_length=200)
    runtime = models.IntegerField()
    release_date = models.DateField()
    synopsis = models.TextField()
    pic = models.ImageField()
    trailer_url = models.URLField()
    
    class Meta:
        verbose_name_plural = "Movies"
    
    def __str__(self):
        return f"{self.last_name}, {self.first_name}"
