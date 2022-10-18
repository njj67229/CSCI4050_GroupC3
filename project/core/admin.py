from django.contrib import admin
from core.models import Movie, Promo, Showing, Genre, PhysicalSeat, SeatInShowing, ShowRoom

# Register your models here.
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'rating', 'poster', 'release_date']
    search_fields = ['title', 'id']

@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    pass

@admin.register(Showing)
class Showing(admin.ModelAdmin):
    pass

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