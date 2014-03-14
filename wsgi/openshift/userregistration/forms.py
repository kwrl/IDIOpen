'''
Created on Feb 26, 2014

@author: filip
'''
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError;
from django import forms
from userregistration.models import CustomUser
from django.utils.translation import ugettext_lazy as _
from contest.models import Invite 

import ipdb;

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = CustomUser
        fields = ("email","first_name","last_name")
        
class CustomStaffUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    def __init__(self, *args, **kargs):
        super(CustomStaffUserCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = CustomUser
        fields = ("email","first_name","last_name", "is_staff", "is_superuser")

class CustomUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = CustomUser
        
        
class RegistrationForm(forms.Form):
    """
    Form for registering a new user account.
    
    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.
    
    Subclasses should feel free to add any additional validation they
    need, but should avoid defining a ``save()`` method -- the actual
    saving of collected user data is delegated to the active
    registration backend.

    """
    required_css_class = 'required'
    
    email = forms.EmailField(label=_("E-mail"))
    first_name = forms.CharField(label=_("First Name"))
    last_name = forms.CharField(label=_("Last Name"))
    password1 = forms.CharField(widget=forms.PasswordInput,
                                label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label=_("Password (again)"))
    
    def clean_email(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        
        """
        existing = User.objects.filter(email__iexact=self.cleaned_data['email'])
        if existing.exists():
            raise forms.ValidationError(_("A user with that email already exists."))
        else:
            return self.cleaned_data['email']

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                ipdb.set_trace()
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data
    
class Invites_Form(forms.Form):
    def clean(self):
        if 'id' in self.cleaned_data and 'submit' in self.cleaned_data:
            if self.cleaned_data['id'].isdigit():
                if self.cleaned_data['submit'] == 'accept':
                    self.cleaned_data['submit'] = True
                elif self.cleaned_data['submit'] == 'decline':
                    self.cleaned_data['submit'] = False
                
                return self.cleaned_data
        
        raise forms.ValidationError(_("The form did not validate"))

class ContestantForm(forms.ModelForm):
    password_validation = forms.CharField(widget=forms.PasswordInput());
    
    def clean(self):
        ipdb.set_trace();
        if self.password_validation != self.Meta.fields['password']:
            raise forms.ValidationError("Passwords do not match");
        
        super(ContestantForm, self).clean();
        return self.cleaned_data;
        
    class Meta:
        fields =['first_name', 'last_name', 'email', 'password'];
        
        widgets = {
                   'password': forms.PasswordInput()
                   };
        
        model = CustomUser;
                