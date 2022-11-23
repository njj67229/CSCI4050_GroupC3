from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.select_show_time, name="select_show_time"),
    path("select_show_time/<int:movie_id>/", views.select_show_time, name="select_show_time"),
    path(
        "select-tickets-and-age",
        views.select_tickets_and_age,
        name="select_tickets_and_age",
    ),
    path("select_seats/<int:show_id>/", views.select_seats, name="select_seats"),
    path("select_seats", views.select_seats, name="select_seats"),
    path("order_summary", views.order_summary, name="order_summary"),
    path("checkout", views.checkout, name="checkout"),
    path("confirmation", views.confirmation, name="confirmation"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
