from atexit import register
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
            return redirect('add_address')
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})

def add_payment(request):
    cards = PaymentCard.objects.filter(card_owner=request.user).all()
    total_cards = cards.count()
    print(total_cards)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        address_form = AddressForm(request.POST)
        if form.is_valid() and address_form.is_valid():
            if total_cards == 3:
                messages.error(request,'You can only add upto 3 cards to your account')
                return redirect('add_payment')
            new_address = address_form.save() #save address first
            new_payment = form.save(commit=False)
    
            user = request.user
            new_payment.card_owner = user
            new_payment.billing_address = new_address
            new_payment = new_payment.save()
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
                # if not user.last_login:
                #     login(request,user)
                #     return redirect(reverse("add_address"))
                # else:
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
    card = PaymentCard.objects.filter(card_owner=request.user).all()
    # select_card_form = SelectCardForm(request.POST or None)
    select_card_form = None
    if card:
        instance = get_object_or_404(CustomUser, username=request.user.username) #user
            #if instance.selected_card:
        card = card[0]
        address = card.billing_address
            #ind = list(select_card_form.fields['usercards'].choices).index(str(card))
            #select_card_form.fields['usercards'].initial = [ind]         
    else:
        return redirect(reverse('add_payment'))
        
    payment_form = PaymentForm(request.POST or None, instance=card)
    address_form = AddressForm(request.POST or None, instance=address)
    #if select_card_form.is_valid() and not payment_form.is_valid():
    #    select_card = select_card_form.save(commit=False)
    #    instance.selected_card = select_card.usercards.all()[0]
    #    return redirect('edit_payments')

    if payment_form.is_valid():
            new_card = payment_form.save(commit=False) #add card to paymentcards table
            new_card.save()
            messages.success(request,'your card has been updated')
            return redirect('edit_payments')
    return render(request,'registration/edit_payment.html',{'form':payment_form, 'address_form':address_form, 'card_form':select_card_form})

#@login_required (login_url='/members/login/')
#def select_card(request)

# @login_required (login_url='/members/login/')
# def edit_cards(request):
#     cards = PaymentCard.objects.filter(card_owner=request.user).all()
#     # select_card_form = SelectCardForm(request.POST or None)
#     if 'card_choice' in request.POST:
#         print(request.POST['card_choice'])
#         card = PaymentCard.objects.filter(pk=int(request.POST['card_choice']))[0]
#         print(card)
#         address = card.billing_address
#         create = 'select'
#     else:
#         if cards:
#             card = cards[0]
#             address = card.billing_address
#             create = 'No'
#         else:
#             card = None
#             address = None
#             create = 'Yes'
#     payment_form = PaymentForm(request.POST or None, instance=card)
#     address_form = AddressForm(request.POST or None, instance=address)
#     print('actual')
#     print(card)
#     print(card.name)
#     if payment_form.is_valid() and 'card_choice' not in request.POST :
#         print('doing the form')
#         #add first payment form here
#         new_address = address_form.save() #save address
#         new_payment = payment_form.save(commit=False)

#         user = request.user
#         new_payment.card_owner = user
#         new_payment.billing_address = new_address
#         new_payment = new_payment.save()
#         if create == 'Yes':
#             messages.success(request,'Your payment information was successfully added')
#         elif create == 'No':
#             messages.success(request,'Your payment information was successfully updated')
        
#         return redirect('edit_cards')
#     return render(request,'registration/edit_payment.html',{'form':payment_form, 'address_form':address_form, 'cards': cards})


@login_required (login_url='/members/login/')
def edit_cards_1(request):
    cards = PaymentCard.objects.filter(card_owner=request.user).all()
    # select_card_form = SelectCardForm(request.POST or None)
    try:
        
        if cards[0]:
            card = cards[0]
            address = card.billing_address
            create = 'No'
        else:
            card = None
            address = None
            create = 'Yes'
        payment_form = PaymentForm(request.POST or None, instance=card)
        address_form = AddressForm(request.POST or None, instance=address)
        print('actual')
        print(card)
        print(card.name)
        if payment_form.is_valid() :
            print('doing the form')
            #add first payment form here
            new_address = address_form.save() #save address
            new_payment = payment_form.save(commit=False)

            user = request.user
            new_payment.card_owner = user
            new_payment.billing_address = new_address
            new_payment = new_payment.save()
            if create == 'Yes':
                messages.success(request,'Your payment information was successfully added')
            elif create == 'No':
                messages.success(request,'Your payment information was successfully updated')
            
            return redirect('edit_cards_1')
        return render(request,'registration/edit_payment.html',{'form':payment_form, 'address_form':address_form, 'cards': cards})
     
    except IndexError:
        payment_form = PaymentForm(request.POST or None, instance=None)
        address_form = AddressForm(request.POST or None, instance=None)
        if payment_form.is_valid() :
            print('doing the form')
            #add first payment form here
            new_address = address_form.save() #save address
            new_payment = payment_form.save(commit=False)

            user = request.user
            new_payment.card_owner = user
            new_payment.billing_address = new_address
            new_payment = new_payment.save()
            if create == 'Yes':
                messages.success(request,'Your payment information was successfully added')
            elif create == 'No':
                messages.success(request,'Your payment information was successfully updated')
            
            return redirect('edit_cards_1')
        return render(request,'registration/edit_payment.html',{'form':payment_form, 'address_form':address_form, 'cards': cards})

@login_required (login_url='/members/login/')
def edit_cards_2(request):
    cards = PaymentCard.objects.filter(card_owner=request.user).all()
    # select_card_form = SelectCardForm(request.POST or None)
    try: 
        if cards[1]:
            card = cards[1]
            address = card.billing_address
            create = 'No'
        else:
            card = None
            address = None
            create = 'Yes'
        payment_form = PaymentForm(request.POST or None, instance=card)
        address_form = AddressForm(request.POST or None, instance=address)
        print('actual')
        print(card)
        print(card.name)
        if payment_form.is_valid() and 'card_choice' not in request.POST :
            print('doing the form')
            #add first payment form here
            new_address = address_form.save() #save address
            new_payment = payment_form.save(commit=False)

            user = request.user
            new_payment.card_owner = user
            new_payment.billing_address = new_address
            new_payment = new_payment.save()
            if create == 'Yes':
                messages.success(request,'Your payment information was successfully added')
            elif create == 'No':
                messages.success(request,'Your payment information was successfully updated')
            
            return redirect('edit_cards_2')
        return render(request,'registration/edit_payment.html',{'form':payment_form, 'address_form':address_form, 'cards': cards})
     
    except IndexError:
        payment_form = PaymentForm(request.POST or None, instance=None)
        address_form = AddressForm(request.POST or None, instance=None)
        return render(request,'registration/edit_payment.html',{'form':payment_form, 'address_form':address_form, 'cards': cards})
    
    
@login_required (login_url='/members/login/')
def edit_cards_3(request):
    cards = PaymentCard.objects.filter(card_owner=request.user).all()
    # select_card_form = SelectCardForm(request.POST or None)
    try:
        
        if cards[2]:
            card = cards[2]
            address = card.billing_address
            create = 'No'
        else:
            card = None
            address = None
            create = 'Yes'
        payment_form = PaymentForm(request.POST or None, instance=card)
        address_form = AddressForm(request.POST or None, instance=address)
        print('actual')
        print(card)
        print(card.name)
        if payment_form.is_valid() and 'card_choice' not in request.POST :
            print('doing the form')
            #add first payment form here
            new_address = address_form.save() #save address
            new_payment = payment_form.save(commit=False)

            user = request.user
            new_payment.card_owner = user
            new_payment.billing_address = new_address
            new_payment = new_payment.save()
            if create == 'Yes':
                messages.success(request,'Your payment information was successfully added')
            elif create == 'No':
                messages.success(request,'Your payment information was successfully updated')
            
            return redirect('edit_cards_3')
        return render(request,'registration/edit_payment.html',{'form':payment_form, 'address_form':address_form, 'cards': cards})
     
    except IndexError:
        payment_form = PaymentForm(request.POST or None, instance=None)
        address_form = AddressForm(request.POST or None, instance=None)
        return render(request,'registration/edit_payment.html',{'form':payment_form, 'address_form':address_form, 'cards': cards})


@login_required (login_url='/members/login/')
def del_payment(request, parameter=None):
    if not PaymentCard.objects.filter(card_owner=request.user).all():
        messages.error(request,'you have no saved cards to your profile')
        return redirect(reverse('edit_cards_1'))
    print(parameter)
    instance = PaymentCard.objects.filter(pk=int(parameter))[0] #user
    instance.delete()
    print(instance)
    messages.success(request,'your card has been deleted')
    return redirect('edit_cards_1')