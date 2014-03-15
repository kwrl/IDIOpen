from django.contrib import admin;
from django.contrib.auth.admin import UserAdmin;
from django.contrib.auth.forms import UserChangeForm;
from django.db import models;
from django.db.models import Q;
from django.utils.translation import ugettext_lazy as _;

import sys, ipdb;

sys.path.append("..")
from userregistration import models as usermodel;

class ContestantManagemenentForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(ContestantManagemenentForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = usermodel.CustomUser;
        
class ContestantManagement(UserAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference the removed 'username' field
    
    def queryset(self, request):
        """ Generate a different view for staff and admins
        """
        qs = super(ContestantManagement, self).queryset(request);
        if request.user.is_superuser:
            return qs;
        return qs.filter(owner=request.user);
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'is_active')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2')}
        ),
    )
    form = ContestantManagemenentForm
    #add_form = CustomUserCreationForm
    list_display = ('email', 'first_name', 'last_name',)
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    
    def queryset(self, request):
        qs = super(UserAdmin, self).queryset(request)
        qs = qs.exclude(Q(is_staff=True) | Q(is_superuser=True))
        return qs
    

    
admin.site.register(usermodel.CustomUser, ContestantManagement);

# EOF