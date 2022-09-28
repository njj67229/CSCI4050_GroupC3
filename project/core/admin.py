from django.contrib import admin
from core.models import Movie, Promo

# Register your models here.
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    pass

@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    pass