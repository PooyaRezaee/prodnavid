from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User
from .forms import *

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm


    list_display = ('full_name','email','is_admin')
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields': ('full_name','email','phone_number','how_meet','password')}),
        ('Permissions', {'fields': ('is_email_active','last_login','is_admin',)}),
    )
    

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('full_name','email', 'phone_number', 'how_meet','password1', 'password2'),
        }),
    )

    search_fields = ('full_name','email')
    ordering = ('full_name',)

admin.site.register(User,UserAdmin)
admin.site.unregister(Group)
