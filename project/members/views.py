from ast import Pass
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from .forms import PaymentForm, SignUpForm, EditProfileForm, PasswordChangeForm, PaymentForm
from django.contrib.auth.views import PasswordChangeView
# from django.contrib.auth.forms import PasswordChangeForm

# Create your views here.
class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('login')

class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('index')
    
    def get_object(self):
        return self.request.user