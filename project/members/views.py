from django.shortcuts import redirect, render
from django.views import generic
from django.urls import reverse, reverse_lazy
from .forms import SignUpForm, EditProfileForm, PasswordChangeForm, PaymentForm, AuthenticationForm
from django.contrib.auth.views import PasswordChangeView
# from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

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

def login(request):
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
    