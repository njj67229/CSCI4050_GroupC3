from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('select-show-time', views.select_show_time, name='select_show_time'),
    path('confirmation', views.confirmation, name='confirmation'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)