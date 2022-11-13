from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns



urlpatterns = [path("", views.index2, name="index"),
               path("home/", views.index2, name='index2'),
               path("home/<str:showing_type>/", views.index2, name='index2')]

urlpatterns += staticfiles_urlpatterns()