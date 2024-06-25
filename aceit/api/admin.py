from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'is_tutor', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    ordering = ('email',)
    filter_horizontal = ()

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
        ('Tutor Status', {'fields': ('is_tutor',)}),
    )

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
