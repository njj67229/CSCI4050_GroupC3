from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('home.urls')),
    path('checkout/', include('checkout.urls')),
    path('admin/', admin.site.urls),
    path('login/', include('login.urls'))
]
