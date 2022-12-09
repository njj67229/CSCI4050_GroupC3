from datetime import datetime, timedelta
from django.db import models
from django.conf import settings
import string
import random
from django.utils.html import mark_safe
from django.core.exceptions import ValidationError

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
    pic = models.ImageField(upload_to='actors/', default="")
    
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
    synopsis = models.TextField(default="")
    pic = models.ImageField(upload_to='images/', default="" )
    trailer_url = models.URLField(default="www.youtube.com")
    producer = models.CharField(max_length=200, null=True)
    director = models.CharField(max_length=200, default="")
    genres = models.ManyToManyField(Genre)
    # actor_ids = models.CharField(max_length=200, null=True, help_text='Ex: [id1, id2, id3, id4, id5]')
    actor_ids = models.ManyToManyField(Actor, verbose_name='Actors')
    
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
        
    @property
    def is_valid(self):
        return self.promo.exp_date >= datetime.now().date()
    
class PhysicalSeat(models.Model):
    seat_row = models.CharField(max_length=1)
    seat_number = models.IntegerField()
    
    def __str__(self):
        return f"{self.seat_row + str(self.seat_number)}"

class SeatInShowing(models.Model):
    physical_seat = models.ForeignKey(PhysicalSeat, on_delete=models.CASCADE)
    reserved = models.BooleanField(default=False)    

    def __str__(self):
        return f"{self.pk} - {self.reserved}"

class ShowRoom(models.Model):
    seats = models.ManyToManyField(PhysicalSeat, null=True)

    def __str__(self):
        return f"{self.pk}"

class Showing(models.Model):
    movie = models.ForeignKey(Movie, on_delete = models.CASCADE)
    showtime = models.DateTimeField()
    room = models.ForeignKey(ShowRoom, on_delete=models.CASCADE)
    seats = models.ManyToManyField(SeatInShowing, blank=True)

    class Meta:
        unique_together = ('showtime', 'room',)

    def __str__(self):
        return f"{self.movie} - {self.showtime.strftime('%a, %B %d - %I:%M %p')}"

    def clean(self):
        showings = Showing.objects.filter(movie__pk=self.movie.id)
        overlap = False
        for showing in showings:
            showingtime = showing.showtime
            runtime = showing.movie.runtime
            showdatetime = self.showtime
            showingtime = showingtime+timedelta(minutes=int(runtime))
            if(showdatetime < showingtime and showing.room == self.room):
                overlap = True
                raise ValidationError({'showtime': "Movie Showings overlap"})
        
        if not overlap:
            self.save()
            room_seats = [] 
            for seat in self.room.seats.all():
                room_seats.append(SeatInShowing.objects.create(physical_seat=seat, reserved=False))
            self.seats.set(room_seats)
            self.save()
            raise ValidationError({'seats': " to confirm"})
