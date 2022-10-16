import imp
from django.urls import include, path
from .views import PasswordsChangeView, UserRegisterView, UserEditView, add_payment, user_login, add_address, add_payment
from django_email_verification import urls as email_urls


urlpatterns = [
   path('register/', UserRegisterView.as_view(), name='register'),
   path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
   path('add_address/', add_address, name='add_address'),
   path('add_payment/', add_payment, name='add_payment'),
   path('password/', PasswordsChangeView.as_view(template_name='registration/change-password.html')),
   path('login/', user_login, name='login'),
   path('email/', include(email_urls)),
   
]
