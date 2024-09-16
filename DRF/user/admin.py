from django.contrib import admin
from django import forms 
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Profile, OTP


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('phone', 'email', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    list_display = ('phone', 'email', 'fullName')
    filter_horizontal = ()
    list_filter = ('is_superuser',)
    fieldsets = ()
    search_fields = ('phone', 'email', 'fullName')
    list_display_links = ('email', 'fullName')
    readonly_fields = ('pk',)
    ordering = ('email', 'pk')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('phone', 'email')


admin.site.register(User, UserAdmin)

admin.site.register(Profile, ProfileAdmin)

admin.site.register(OTP)
