from django.shortcuts import redirect, render
from django.views import generic
from django.urls import reverse, reverse_lazy
from .forms import SignUpForm, EditProfileForm, PasswordChangeForm,AuthenticationForm
from accounts.forms import AddressForm, PaymentForm 
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.
def add_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            new_payment = form.save()
            request.user.paymentcards = new_payment
            request.user.paymentcards.set([new_payment])
            request.user.save()
            messages.success(request,'your payment information was successfully added')
    else:
        form = PaymentForm()
    return render(request,'registration/add_payment.html',{'form':form})

def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            new_address = form.save()
            request.user.address = new_address
            request.user.save()
            messages.success(request,'your address was successfully added')
    else:
        form = AddressForm()
    return render(request,'registration/add_address.html',{'form':form})
    
class PasswordsChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('login')

class UserRegisterView(SuccessMessageMixin, LoginRequiredMixin, generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('add_address')
    success_message = 'Your account was successfully created'
    
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
  
class UserEditView(SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('edit_profile')
    success_message = 'Your account was successfully updated'
    
    def get_object(self):
        return self.request.user

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user:
            print(user.status)
            #check if super_user and redirect to admin portal
            if user.is_superuser:
                return redirect(('admin:index'))
            #check is user is active
            if user.status.id == 1:
                login(request,user)
                return redirect(reverse('index'))
            # Check if inactive
            if user.status.id == 2:
                print(user.status.id)
                messages.error(request,'your account needs to be verified')
                return redirect(reverse('login'))
            #check if suspended
            if user.status.id == 3:
                messages.error(request,'your account account has been suspended. Contact admin for more information')
                return redirect(reverse('login'))        
        else:
            messages.error(request,'username or password not correct')
            return redirect(reverse('login'))
    else:
        form = AuthenticationForm()
    return render(request,'registration/login.html',{'form':form})
    