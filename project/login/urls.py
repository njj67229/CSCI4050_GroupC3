from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register', views.register, name='register'),
    path('account_confirmation', views.account_confirmation, name='account_confirmation'),
    path('login', views.login, name='login'),
    path('edit_profile', views.edit_profile, name='edit_profile')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)