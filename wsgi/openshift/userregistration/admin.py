from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from openshift.userregistration.models import CustomUser
from openshift.userregistration.forms import *


class Admin(CustomUser):
    class Meta:
        proxy = True
        app_label = 'auth'
        verbose_name = 'Admin account'
        verbose_name_plural = 'Admin accounts'

class Contestant(CustomUser):
    class Meta:
        proxy = True
        app_label = 'contest'
        verbose_name = 'Contestant'
        verbose_name_plural = 'Contestants'

class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference the removed 'username' field
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name','nickname', 'is_active','is_staff',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2')}
        ),
    )
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('email', 'first_name', 'last_name',)
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    
    def queryset(self, request):
        qs = super(UserAdmin, self).queryset(request)
        qs = qs.exclude(Q(is_staff=True) | Q(is_superuser=True))
        return qs


class CustomStaffAdmin(UserAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference the removed 'username' field
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name','nickname')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2')}
        ),(_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
    )
    form = CustomUserChangeForm
    add_form = CustomStaffUserCreationForm
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    
    def queryset(self, request):
        qs = super(UserAdmin, self).queryset(request)
        qs = qs.filter(Q(is_staff=True) | Q(is_superuser=True))
        return qs

admin.site.register(Contestant, CustomUserAdmin)
admin.site.register(Admin, CustomStaffAdmin)
