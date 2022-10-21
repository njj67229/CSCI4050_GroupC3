from re import template
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
   path('password/', 
        PasswordsChangeView.as_view(template_name='registration/change-password.html'),
        name='password'),
   path('password_reset/', 
        auth_views.PasswordResetView.as_view(template_name='registration/pswd/password_reset.html'), 
        name='password_reset'),
   path('password_reset/done/', 
        auth_views.PasswordResetDoneView.as_view(template_name='registration/pswd/password_reset_done.html'), 
        name='password_reset_done'),
   path('reset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(template_name='registration/pswd/password_reset_confirm.html'), 
        name='password_reset_confirm'),
   path('reset/done/', 
        auth_views.PasswordResetCompleteView.as_view(template_name='registration/pswd/password_reset_complete.html'),
        name="password_reset_complete"),
   path('login/', user_login, name='login'),
   path('email/', include(email_urls)),
   
]
