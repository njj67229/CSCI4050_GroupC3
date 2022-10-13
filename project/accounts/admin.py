from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Address, PaymentCard

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['pk',"email", "username", "first_name", "last_name"]
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'first_name', 'last_name', 'address','paymentcards', 'receive_promos'),})
    )
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('address','receive_promos', 'paymentcards')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Address)
class Address(admin.ModelAdmin):
    pass

@admin.register(PaymentCard)
class PaymentCard(admin.ModelAdmin):
    pass
