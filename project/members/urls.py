from django.urls import include, path
from .views import PasswordsChangeView, UserRegisterView, UserEditView, add_payment, user_login, add_address, add_payment, edit_address, del_address
from django_email_verification import urls as email_urls
from django.contrib.auth import views as auth_views


urlpatterns = [
   path('register/', UserRegisterView.as_view(), name='register'),
   path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
   path('add_address/', add_address, name='add_address'),
   path('edit_address/', edit_address, name='edit_address'),
   path('del_address/', del_address, name='del_address'),
   path('add_payment/', add_payment, name='add_payment'),
   path('password/', PasswordsChangeView.as_view(template_name='registration/change-password.html'), name='password'),
   path('login/', user_login, name='login'),
   path('email/', include(email_urls)),
   
]
