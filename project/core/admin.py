from django.contrib import admin
from core.models import Movie, Promo, Showing, Genre, MPAA

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
