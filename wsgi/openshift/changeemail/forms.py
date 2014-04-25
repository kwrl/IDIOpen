""" This file defines a form to change an email based 
    on a given User model.

    The form asks for an email validation 
    (i.e. the user has to enter the mail twice).
"""

from django import forms
from django.core.exceptions import ValidationError
from django.forms.util import ErrorList

from .models import ChangeEmail

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User


def append_field_error(instance, field, message):
    instance.errors[field] = ErrorList()
    instance.errors[field].append(message)

class EmailForm(forms.Form):
    """ Form to update the email of activated contestants
    """
    email = forms.EmailField(label=u'New Email')
    email_validation = forms.EmailField(label=u'Repeat New Email')

    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)
        """ HTML context name
        """
        self.contextName = "useremail"

    def clean(self):
        """ Ensure fields are non-empty
            and that they match each other
        """
        # Ensure fields are non-empty
        if  'email'            in self.cleaned_data \
        and 'email_validation' in self.cleaned_data:
            email = self.cleaned_data['email']
            email_validation = self.cleaned_data['email_validation']

            if email != email_validation:
                # Append error, emails do not match
                self.errors['email'] = ErrorList()
                self.errors['email_validation'] = ErrorList()
                self.errors['email'].append("%s do not match"
                                                % ("emails"))
                self.errors['email_validation'].append("%s do not match"
                                                           % ("emails"))
            else:
                super(EmailForm, self).clean()
                if not self.__isEmailUnique(email):
                    append_field_error(self, 'email',
                                        "Email already exists in the database"
                                        + ", please use another")
                    raise ValidationError("")
                return self.cleaned_data

        raise ValidationError("Fields cannot be empty")

    def __isEmailUnique(self, sug_email):
        """ Verify that the suggested email does not already exist in the
            userbase
        """
        if User.objects.filter(email=sug_email).count():
            return False

        return True

    def save(self, user, request):
        """ We want to send an email, instead of saving to model.
        """
        realUser = User.objects.get(pk=user.pk)
        new_email = ChangeEmail()
        new_email.save(realUser, self.cleaned_data['email'])
        new_email.send_confirmation_mail(request)

# EOF
