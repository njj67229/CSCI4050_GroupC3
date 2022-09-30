from django.urls import path
from . import views
<<<<<<< HEAD

urlpatterns = [
    path("", views.home, name="home")]
=======
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index')
]
>>>>>>> front-end
