from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from creditcards.forms import CardNumberField, CardExpiryField, SecurityCodeField

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ("username", "email")

class CustomUserChangeForm(UserChangeForm):
    receive_promos = forms.BooleanField(required=False)
    class Meta:
        model = CustomUser
        fields = ("username", "email")

class PaymentForm(forms.Form):
    name_on_card = forms.CharField(max_length=50, required=True)
    cc_number = CardNumberField(label='Card Number', required=True)
    cc_expiry = CardExpiryField(label='Expiration Date', required=True)
    cc_code = SecurityCodeField(label='CVV/CVC', required=True)