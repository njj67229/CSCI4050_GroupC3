from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from creditcards.forms import CardNumberField, CardExpiryField, SecurityCodeField
from .models import CustomUser, Address, PaymentCard

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")

class CustomUserChangeForm(UserChangeForm):
    receive_promos = forms.BooleanField(required=False)
    class Meta:
        model = CustomUser
        fields = ("username", "email")

class PaymentForm(forms.ModelForm):
    cc_code = forms.CharField(widget=forms.PasswordInput(), max_length=4)
    class Meta:
        model = PaymentCard
        fields = "__all__"

class AddressForm(forms.ModelForm):
    
    class Meta:
        model = Address
        fields = "__all__"