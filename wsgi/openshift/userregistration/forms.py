#pylint: disable=C0103, E1002, W0232, C1001, R0903
'''
Created on Feb 26, 2014
@author: filip
'''
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django import forms
from django.forms.util import ErrorList
from .models import CustomUser, YEAR_OF_STUDY, GENDER_CHOICES
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_variables
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.template import loader
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


'''
By: Typo. As far as i can tell this import is not used.
And i have to remove them in order to make testing work..

Forget that...
No, dont forget that 
'''  

'''
from changeemail.models import ChangeEmail
from changeemail.forms import EmailForm
'''

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User


def append_field_error(instance, field, message):
    instance.errors[field] = ErrorList()
    instance.errors[field].append(message)

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
    nickname = forms.CharField(label=
                               _("Nickname (optional)"),
                               required=False)
    password1 = forms.CharField(widget=forms.PasswordInput,
                                label=_("New password"))
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label=_("New Password (again)"))

    skill_level = forms.ChoiceField(label="Year of study",
                                  choices=YEAR_OF_STUDY,
                                  initial=YEAR_OF_STUDY[-1][0])
    gender = forms.ChoiceField(label="Gender",
                             choices=GENDER_CHOICES,
                             initial=GENDER_CHOICES[0][0])

    def clean_email(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.

        """
        existing = User.objects.filter(email__iexact=self.cleaned_data['email'])
        if existing.exists():
            raise forms.ValidationError(
                    _("A user with that email already exists."))
        else:
            return self.cleaned_data['email']
 
 #===============================================================================
 # Strips trailing whitespace from first_name, last_name and nickname.
 # Note: Not the best solution, but didn't manage to do this in the model instead.
 #===============================================================================
 
    def clean_first_name(self):        
        first_name = self.cleaned_data.get('first_name')
        
        if first_name.isspace():        
            raise ValidationError("First name not set")
        else:
            return self.cleaned_data['first_name'].strip()   
            
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        
        if last_name.isspace():
            raise ValidationError("Last name not set")
        else:
            return self.cleaned_data['last_name'].strip()
        
    def clean_nickname(self):
        """Ensures that nicknames are not all spaces"""
        nickname = self.cleaned_data.get('nickname')
        
        if nickname.isspace():        
            raise ValidationError("Nickname not set")
        else:
            return self.cleaned_data['nickname'].strip() 

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.

        """
        cleaned_data = super(RegistrationForm, self).clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2:
            if password1 != password2:
                append_field_error(self, 'password1',
                        _("The two passwords didn't match"))
                append_field_error(self, 'password2',
                        _("The two passwords didn't match"))
                raise forms.ValidationError('')
            
            try:
                tmpCU = User()
                tmpCU.clean_password(password1)
            except ValidationError as ve:
                append_field_error(self, 'password1',
                               _(ve.message))
                raise forms.ValidationError('')
            return cleaned_data
            
        else:
            append_field_error(self, 'password1',
                        _("Please write a password"))
                        
'''
Form for showing the invites
'''
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

class PasswordForm(forms.ModelForm):
    """ A form to update the password for an activated user.
        Uses an extra field, password_validation, to prevent user errors.
    """
    password_validation = forms.CharField(widget=forms.PasswordInput(),
                                          label=u'Password (confirm)')
    old_password = forms.CharField(widget=forms.PasswordInput(),
                                   label=u'Old password')

    def __init__(self, *args, **kwargs):
        """ Initialize, and explicitly set the order of the fields
        """
        super(PasswordForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = ['old_password',
                'password', 'password_validation']

        self.contextName = "userpw"
        """ For HTML context
        """

    @sensitive_variables('old_password', 'password', 'password_validation')
    def clean(self):

        # Ensure fields are non-empty
        if 'old_password' in self.cleaned_data:
            oldpw = self.cleaned_data['old_password']
            if not self.instance.check_password(oldpw):
                append_field_error(self, 'old_password', "Incorrect password")
                raise ValidationError("")


        if  'password'            in self.cleaned_data \
        and 'password_validation' in self.cleaned_data:
            pw = self.cleaned_data['password']
            pw_validation = self.cleaned_data['password_validation']

            if pw != pw_validation:
                append_field_error(self, 'password', u"Passwords don\'t match")
                append_field_error(self, 'password_validation',
                                   u"Passwords don\'t match")
            else:
                # in case someone adds other fields, we explicitly invoke
                # super.clean. However, it is not needed per march
                super(PasswordForm, self).clean()
                try:
                    self.instance.clean_password(pw)
                except ValidationError as ve:
                    append_field_error(self, 'password', _(ve.message))
                return self.cleaned_data

        raise ValidationError("Fields cannot be empty")

    def save(self):
        """ Ensure that the password is hashed before updating it in the model
        """
        pw = self.cleaned_data['password']
        self.instance.set_password(pw)
        self.instance.save()
        
    class Meta:
        model = CustomUser
        fields = ['password']
        help_texts = {
                'password_validation': "Enter password again for validation",
            }
        widgets = {
                'password' : forms.PasswordInput()
            }

class PIForm(forms.ModelForm):
    """ Form to update the personal information of activated contestants
    """
    def save(self):
        super(PIForm, self).save()

    def __init__(self, *args, **kwargs):
        super(PIForm, self).__init__(*args, **kwargs)
        """ HTML context name
        """
        self.contextName = "userpi"

    class Meta:
        model   = CustomUser
        fields  = ['first_name', 'last_name', 'nickname',
                   'skill_level', 'gender']
        labels = {
                'skill_level': "Year of Study",
                    };
        help_text = {
                     'first_name': "First name",
                     'last_name':"Last name",
                     }
        
class PasswordResetForm(forms.Form):
    email = forms.EmailField(label=_("Email"), max_length=254)

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        from django.core.mail import send_mail
        UserModel = get_user_model()
        email = self.cleaned_data["email"]
        active_users = UserModel._default_manager.filter(
            email__iexact=email, is_active=True)
        url = request.path.split('/')[1]
        for user in active_users:
            # Make sure that no email is sent to a user that actually has
            # a password marked as unusable
            if not user.has_usable_password():
                continue
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
                'url': url,
            }
            subject = loader.render_to_string(subject_template_name, c)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            email = loader.render_to_string(email_template_name, c)
            send_mail(subject, email, from_email, [user.email])


# EOF

