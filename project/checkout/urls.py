from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import ListView

urlpatterns = [
    path("", views.select_show_time, name="select_show_time"),
    path("select_show_time/<int:movie_id>/", views.select_show_time, name="select_show_time"),
    path(
        "select_tickets_and_age/<str:seats>/<int:show_id>",
        views.select_tickets_and_age,
        name="select_tickets_and_age",
    ),
    path("select_seats/<int:show_id>/", views.select_seats, name="select_seats"),
    path("select_seats", views.select_seats, name="select_seats"),
    path("order_summary/<int:ad>/<int:ch>/<int:sr>/<str:seats>/<int:show_id>", views.order_summary, name="order_summary"),
    path("checkout/<int:ad>/<int:ch>/<int:sr>/<str:seats>/<int:show_id>", views.checkout, name="checkout"),
    path("order_history", views.order_history, name="order_history"),
    path("confirmation", views.confirmation, name="confirmation"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
