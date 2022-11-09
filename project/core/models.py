from datetime import datetime, timedelta
from django.db import models
from django.conf import settings
import string
import random
from django.utils.html import mark_safe

User = settings.AUTH_USER_MODEL

def get_code(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
    
# Create your models here.
class Genre(models.Model):
    
    title = models.CharField(max_length=200, unique=True)
    
    def __str__(self):
        return f"{self.title}"

class MPAA(models.Model):
    
    rating = models.CharField(max_length=200, unique=True)
    
    class Meta:
        verbose_name_plural = "MPAA Rating"
    
    def __str__(self):
        return f"{self.rating}"
    
class Actor(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=200)
    pic = models.ImageField(upload_to='actors/')
    
    def __str__(self):
        return f"{self.name}"
    
    def actor_pic(self):
                if self.pic != '':
                    return mark_safe('<img src="%s%s" width="50" height="75" />' % (f'{settings.MEDIA_URL}', self.pic))
    
class Movie(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    title = models.CharField(max_length=200)
    tag = models.TextField()
    rating = models.ForeignKey(MPAA, on_delete = models.CASCADE)
    runtime = models.CharField(max_length=200, null=True, help_text='in mins')
    release_date = models.DateField(null=True)
    synopsis = models.TextField()
    pic = models.ImageField(upload_to='images/')
    trailer_url = models.URLField(default="www.youtube.com")
    producer = models.CharField(max_length=200)
    director = models.CharField(max_length=200)
    genres = models.ManyToManyField(Genre)
    # actor_ids = models.CharField(max_length=200, null=True, help_text='Ex: [id1, id2, id3, id4, id5]')
    actor_ids = models.ManyToManyField(Actor, verbose_name='Actors', null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Movies"
    
    def __str__(self):
        return f"{self.title}"
    
    def poster(self):
                if self.pic != '':
                    return mark_safe('<img src="%s%s" width="50" height="75" />' % (f'{settings.MEDIA_URL}', self.pic))

class Promo(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=6, default=get_code())
    discount = models.DecimalField(decimal_places=2, max_digits=3, default=0.1)
    exp_date = models.DateField(default= datetime.now()+ timedelta(days=30))
    
    def __str__(self):
        return f"{self.name}"       
    
    def is_expired(self):
        self.objects.filter(self.exp_date < datetime.datetime.now().date())
    
class PhysicalSeat(models.Model):

    def __str__(self):
        return f"{self.pk}"

class SeatInShowing(models.Model):
    physical_seat = models.OneToOneField(PhysicalSeat, primary_key=True, on_delete=models.CASCADE, unique=True)
    reserved = models.BooleanField()    

    def __str__(self):
        return f"{self.pk} - {self.reserved}"

class ShowRoom(models.Model):
    seats = models.ManyToManyField(PhysicalSeat)

    def __str__(self):
        return f"{self.pk}"

class Showing(models.Model):
    movie = models.ForeignKey(Movie, on_delete = models.CASCADE)
    showtime = models.DateTimeField()
    room = models.ForeignKey(ShowRoom, on_delete=models.CASCADE)
    seats = models.ManyToManyField(SeatInShowing)

    def __str__(self):
        return f"{self.movie} - {self.showtime}"