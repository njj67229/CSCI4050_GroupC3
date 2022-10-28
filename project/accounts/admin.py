from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Address, CustomerSatus, PaymentCard
from core.models import Promo
from django.core.mail import send_mail
from django.contrib import messages


@admin.action(description="Send promos to users")
def send_promo(modeladmin, request, queryset):
    """Sends Promos to Selected Users"""
    latest_promo = Promo.objects.last()
    email_list = [user.email for user in queryset]

    send_mail(
        "New Promo Code Added",
        latest_promo.name,
        "teamc3movies@gmail.com",
        email_list,
        fail_silently=False,
    )
    messages.add_message(request, messages.SUCCESS, "Emails Have Been Sent")


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "pk",
        "email",
        "username",
        "first_name",
        "last_name",
        "is_superuser",
        "status",
    ]
    list_filter = ("status", "receive_promos")
    actions = [send_promo]
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('email', 'first_name', 'last_name', 'profile_pic','address', 'status', 'receive_promos'),}),
    )
    fieldsets = UserAdmin.fieldsets + (
        (None,  {'fields': ('address','status', 'profile_pic' ,'receive_promos')}),
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
