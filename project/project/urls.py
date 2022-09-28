from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('checkout/', include('checkout.urls')),
    path('admin/', admin.site.urls),
    path("", include('home.urls')),
]
