from django.contrib import admin
from core.models import Movie, Promo, Showing, Genre, PhysicalSeat, SeatInShowing, ShowRoom, MPAA, Actor

# Register your models here.
@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ['name', 'actor_pic', 'id']
    search_fields = ['name', 'id']
    
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'rating', 'poster', 'release_date']
    search_fields = ['title', 'id']
    filter_horizontal = ('actor_ids',)
    ordering = ['title']
    list_filter = ("genres",)

@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    pass

@admin.register(Showing)
class Showing(admin.ModelAdmin):
    # fields = ('movie', 'showtime', 'room')
    exclude = ('seats',)
    # pass

@admin.register(Genre)
class Genre(admin.ModelAdmin):
    pass

@admin.register(MPAA)
class MPAA(admin.ModelAdmin):
    pass

@admin.register(PhysicalSeat)
class PhysicalSeat(admin.ModelAdmin):
    pass

@admin.register(SeatInShowing)
class SeatInShowing(admin.ModelAdmin):
    pass

@admin.register(ShowRoom)
class ShowRoom(admin.ModelAdmin):
    pass