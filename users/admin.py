from django.contrib import admin
from .models import MyUser ,Contact
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
# Register your models here.

admin.site.register(Contact)

class CaretionUserFroms(forms.ModelForm):
    password1 = forms.CharField(label="passwor",widget=forms.PasswordInput)
    password2 = forms.CharField(label="password confirm" ,widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ("username","email","first_name","last_name",)

def clean_password2(self):
    password1 = self.cleaned_data.get("password1")
    password2 = self.cleaned_data.get("password2")

    if password1 and password2 and password1 != password2:
        raise ValidationError("Passwords don't match")
    return password2


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ("username","email","first_name","last_name","is_active","is_admin","is_staff","is_superuser")

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = CaretionUserFroms

    list_display = ("username","email","first_name","last_name","is_admin","is_active","is_staff","is_superuser")
    list_filter = ()

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "bio")}),
        ("Permissions", {"fields": ("is_active", "is_admin", "is_staff","is_superuser")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "first_name", "last_name", "password1", "password2"),
        }),
    )

    search_fields = ["username","email"]
    filter_horizontal = ()


admin.site.register(MyUser,UserAdmin)
admin.site.unregister(Group)