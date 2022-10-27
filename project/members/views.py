from django.shortcuts import redirect, render
from django.views import generic
from django.urls import reverse, reverse_lazy
from .forms import SignUpForm, EditProfileForm, PasswordChangeForm,AuthenticationForm
from accounts.forms import AddressForm, PaymentForm 
from django.contrib.auth.views import PasswordChangeView, PasswordResetView
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.messages.views import SuccessMessageMixin
from accounts.models import Address, CustomUser, CustomerSatus, PaymentCard
from accounts.forms import AddressForm
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.http import HttpResponse
from django.template import loader
from .tokens import account_activation_token

# Create your views here.
def add_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        address_form = AddressForm(request.POST)
        if form.is_valid() and address_form.is_valid():
            new_address = address_form.save()
            new_payment = form.save(commit=False)
            #form.billing_address = new_address  
            instance = request.user
            new_payment.card_owner = instance
            new_payment.billing_address = new_address
            new_payment = new_payment.save()
            instance.paymentcards.set([new_payment])
            instance = instance.save()
            messages.success(request,'Your payment information was successfully added')
    else:
        form = PaymentForm()
        address_form = AddressForm()
    return render(request,'registration/add_payment.html',{'form':form, 'address_form':address_form})

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
    """Handles password change view"""
    form_class = PasswordChangeForm
    success_url = reverse_lazy('login')

def signup(request):
    "Handles Registration and sends activation email"
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            #ADD REST OF THE FIELDS FOR USER
            #CARD, ADDRESS ETC
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Verify your Account'
            message = render_to_string('registration/mail_body.html', {
                'user': user.first_name,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            messages.info(request,'Please check your email address to complete the registration')
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})


def activate(request, uidb64, token):
    """Handles the verification process and sets status to active"""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.status = CustomerSatus.objects.get(pk=1)
        user.save()
        messages.success(request,'Thank you for your email confirmation. Now you can login your account.')
        return redirect('login')
    else:
        messages.error(request,'Activation link is invalid!')
        return redirect('signup')
  
class UserEditView(SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
    "Personal Info Edit View"
    form_class = EditProfileForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('edit_profile')
    success_message = 'Your account was successfully updated'
    
    def get_object(self):
        return self.request.user

@login_required (login_url='/members/login/')
def edit_address(request): 
    # instance = get_object_or_404(CustomUser, address=request.user.address)
    if request.user.address:
        instance = get_object_or_404(CustomUser, address=request.user.address) #address
        instance = instance.address
        create = False
    else:
        instance = None
        create = True
    form = AddressForm(request.POST or None, instance=instance)
    if form.is_valid():
          new_address = form.save() #added/updated to address table
          if create: #need to add to user
            request.user.address = new_address
            request.user.save()
          messages.success(request,'your address has been updated')
          return redirect('edit_address')
    return render(request,'registration/edit_address.html',{'form':form})

@login_required
def del_address(request):
    if not request.user.address:
        messages.error(request,'you have no saved address to your profile')
        return redirect(reverse('edit_address'))
        
    instance = get_object_or_404(CustomUser, address=request.user.address) #user
    instance.address.delete()
    messages.success(request,'your address has been deleted')
    return redirect('edit_address')

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
                login(request,user)
                return redirect(('admin:index'))
            #check is user is active
            if user.status.id == 1:
                if not user.last_login:
                    login(request,user)
                    return redirect(reverse("add_address"))
                else:
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

@login_required (login_url='/members/login/')
def edit_payments(request): 
    if request.user.paymentcard1:
        instance = get_object_or_404(CustomUser, paymentcard1=request.user.paymentcard1) #user
        card = instance.paymentcard1 #card1
        create = False
    else:
        card = None
        create = True
    form = PaymentForm(request.POST or None, instance=card)
    if form.is_valid():
          new_card = form.save(commit=False) #add card to paymentcards table
          if create:
            request.user.paymentcard1 = new_card
            request.user.save()
          new_card.save()
          messages.success(request,'your card has been updated')
          return redirect('edit_payments')
    return render(request,'registration/edit_payment.html',{'form':form})