from django.contrib import admin
from core.models import Movie, Promo, Showing, Genre, MPAA, Profile

# Register your models here.
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    pass

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

@admin.register(Profile)
class Profile(admin.ModelAdmin):
    pass