from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('select-show-time', views.select_show_time, name='select_show_time'),
    path('select-tickets-and-age', views.select_tickets_and_age, name='select_tickets_and_age'),
    path('select-seats', views.select_seats, name='select_seats'),
    path('payment', views.payment, name='payment'),
    path('confirmation', views.confirmation, name='confirmation'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)