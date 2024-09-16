from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Profile


class UserAdmin(BaseUserAdmin):
    list_display = ('phone', 'email', 'fullName')
    filter_horizontal = ()
    list_filter = ('is_superuser', 'is_active')
    fieldsets = ()
    search_fields = ('phone', 'email', 'fullName')
    list_display_links = ('email', 'fullName')
    readonly_fields = ('pk',)
    ordering = ('email', 'pk')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('phone', 'email')


admin.site.register(User, UserAdmin)

admin.site.register(Profile, ProfileAdmin)
