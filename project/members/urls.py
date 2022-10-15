import imp
from django.urls import include, path
from .views import PasswordsChangeView, UserRegisterView, UserEditView, user_login
from django_email_verification import urls as email_urls


urlpatterns = [
   path('register/', UserRegisterView.as_view(), name='register'),
   path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
   path('password/', PasswordsChangeView.as_view(template_name='registration/change-password.html')),
   path('login/', user_login, name='login'),
   path('email/', include(email_urls)),
   
]
