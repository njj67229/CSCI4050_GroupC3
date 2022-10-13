from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('home.urls')),
    path('checkout/', include('checkout.urls')),
    path('admin/', admin.site.urls),
    path('login/', include('login.urls')),
    path('members/', include('members.urls')),
    path('members/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)