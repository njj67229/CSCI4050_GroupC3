import imp
from django.urls import path
from .views import PasswordsChangeView, UserRegisterView, UserEditView, login


urlpatterns = [
   path('register/', UserRegisterView.as_view(), name='register'),
   path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
   path('password/', PasswordsChangeView.as_view(template_name='registration/change-password.html')),
   path('login/', login, name='login')
   
]
