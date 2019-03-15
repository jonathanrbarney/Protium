from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import *
from accounts.models import Account

class AccountAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password', 'usafa_id')}),
        (('Personal info'), {'fields': ('account_type','email', 'first_name', 'middle_name', 'last_name', 'dob',
                                        'phone_number', 'gender', 'official_email', 'official_phone_number',
                                        'profile_pic', 'room_number', 'last_four', 'building', 'SSN', 'class_year',
                                        'academic_advisor','discus_id')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                      'groups', 'user_permissions')}),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields=['usafa_id']
    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2')}),
        (('Personal info'), {'fields': ('account_type','email', 'first_name', 'middle_name', 'last_name', 'dob',
                                        'phone_number', 'gender', 'official_email', 'official_phone_number',
                                        'profile_pic','discus_id','hometown')}),
        (('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                      'groups', 'user_permissions')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'usafa_id')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(Account, AccountAdmin)
app_models = apps.get_app_config('accounts').get_models()


for model in app_models:
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass