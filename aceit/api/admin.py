from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import *

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'profile_picture', 'is_tutor', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    ordering = ('email',)
    filter_horizontal = ()

    add_fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'profile_picture')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
        ('Tutor Status', {'fields': ('is_tutor',)}),
    )


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject_name', 'education_level', 'pathway', 'track', 'grade')
    search_fields = ('subject_name', 'education_level', 'pathway', 'track', 'grade')
    list_filter = ('education_level', 'pathway', 'track', 'grade')


admin.site.register(User, UserAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Test)
admin.site.register(Question)
admin.site.unregister(Group)
