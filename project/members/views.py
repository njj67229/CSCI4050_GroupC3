import email
import django
from django.shortcuts import redirect, render
from django.views import generic
from django.urls import reverse, reverse_lazy
from .forms import SignUpForm, EditProfileForm, PasswordChangeForm,AuthenticationForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django_email_verification import send_email

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

# Create your views here.
class PasswordsChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('login')

class UserRegisterView(LoginRequiredMixin, generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        user = form.save()
        returnVal = super(UserRegisterView, self).form_valid(form)
        template = render_to_string('registration/mail_body.html', {'name': user.first_name})
        print('here')
        email = EmailMessage(
            'Verify your Account',
            template,
            settings.EMAIL_HOST_USER,
            [user.email]
        )
        email.fail_silently=False
        email.send()
        
        return returnVal
  
class UserEditView(LoginRequiredMixin, generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('index')
    
    def get_object(self):
        return self.request.user

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user:
            print(str(user.status))
            if str(user.status) != "('Inactive', 2)":
                login(request,user)
                return redirect(reverse('index'))
            else:
                messages.error(request,'your account needs to be verified')
                return redirect(reverse('login'))
                
        else:
            messages.error(request,'username or password not correct')
            return redirect(reverse('login'))
    else:
        form = AuthenticationForm()
    return render(request,'registration/login.html',{'form':form})
    