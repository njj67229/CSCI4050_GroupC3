from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Address, CustomerSatus, PaymentCard

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['pk',"email", "username", "first_name", "last_name", "is_superuser", 'status']
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'first_name', 'last_name', 'profile_pic','address', 'paymentcard1','paymentcard2', 'paymentcard3','status', 'receive_promos'),}),
    )
    fieldsets = UserAdmin.fieldsets + (
        (None,  {'fields': ('address','status', 'profile_pic' ,'receive_promos','paymentcard1','paymentcard2', 'paymentcard3',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Address)
class Address(admin.ModelAdmin):
    pass

@admin.register(PaymentCard)
class PaymentCard(admin.ModelAdmin):
    pass

@admin.register(CustomerSatus)
class CustomerStatus(admin.ModelAdmin):
    pass