import hashlib
import random
import re

from django.db import models
from django.core.exceptions import ValidationError;
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.template.loader import render_to_string



'''
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

'''
class CustomUserManager(BaseUserManager):
    def _create_user(self, email, first_name, last_name, password, skill_level, 
                     gender, nickname, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name,
                          last_name=last_name, nickname=nickname,
                          gender=gender, skill_level=skill_level,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, first_name, last_name,
                    password, skill_level, gender, nickname, **extra_fields):
        return self._create_user(email, first_name, last_name, password,
                                skill_level, gender, nickname,
                                 False, False, **extra_fields)

    def create_superuser(self, email,
                         first_name, last_name, password, **extra_fields):
        return self._create_user(email, first_name, last_name, password,
                                skill_level='1', gender='M', nickname="",
                                is_staff=True, is_superuser=True, **extra_fields)
    def activate_user(self, activation_key):
        """
        Validate an activation key and activate the corresponding
        ``User`` if valid.

        If the key is valid and has not expired, return the ``User``
        after activating.

        If the key is not valid or has expired, return ``False``.

        If the key is valid but the ``User`` is already active,
        return ``False``.

        To prevent reactivation of an account which has been
        deactivated by site administrators, the activation key is
        reset to the string constant ``RegistrationProfile.ACTIVATED``
        after successful activation.

        """
        # Make sure the key we're trying conforms to the pattern of a
        # SHA1 hash; if it doesn't, no point trying to look it up in
        # the database.
        SHA1_RE = re.compile('^[a-f0-9]{40}$')
        if SHA1_RE.search(activation_key):
            try:
                user = self.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                return False
            user.is_active = True
            user.activation_key = self.model.ACTIVATED
            user.save()
            return user
        return False

    def create_inactive_user(self, email,first_name, last_name, password,
                             site, url, skill_level, gender, nickname,
                             send_email=True):
        """
        Create a new, inactive ``User``, generate a
        ``RegistrationProfile`` and email its activation key to the
        ``User``, returning the new ``User``.

        By default, an activation email will be sent to the new
        user. To disable this, pass ``send_email=False``.

        """
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        username = email
        if isinstance(email, unicode):
            username = email.encode('utf-8')
        activation_key = hashlib.sha1(salt+username).hexdigest()
        new_user = self.create_user(email,first_name, last_name, password,
                                    skill_level, gender, nickname);
        new_user.is_active = False
        new_user.activation_key = activation_key
        new_user.save()

        if send_email:
            new_user.send_activation_email(site, url)

        return new_user;

YEAR_OF_STUDY = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('Pro', 'Pro'),
    );
GENDER_CHOICES = (
            (' ', 'Not specified'),
            ('M', 'Male'),
            ('F', 'Female'),
    );
MINIMUM_PASSWORD_LENGTH = 6;

class CustomUser(AbstractBaseUser, PermissionsMixin):
    skill_level = models.CharField(max_length=4, choices=YEAR_OF_STUDY,
                                  default=YEAR_OF_STUDY[0][0]);
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,
                             default=GENDER_CHOICES[0][0]);
    """
    A fully featured User model with admin-compliant permissions that uses
    a full-length email field as the username.

    Email and password are required. Other fields are optional.
    """
    email       = models.EmailField(_('email address'), max_length=254,
                                    unique=True)
    """ email used when an activated user changes his/her email
    """
    temp_email  = models.EmailField(_('temp email'), max_length=254,
                                    unique=False, null=True, blank=True)

    email_activation_key = models.CharField(max_length=40,
                                            null=True);
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    ACTIVATED = u"ALREADY_ACTIVATED"
    activation_key = models.CharField(_('activation key'), max_length=40)
    objects = CustomUserManager()
    nickname = models.CharField(_('nickname'), max_length=20, default='',
                                null=True, blank=True);

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']


    # password = models.CharField(_('password'), max_length=128,
    #                             validators=[MinLengthValidator(
    #                                                  MINIMUM_PASSWORD_LENGTH)]);

    def clean_password(self, pw):
        #FIXME: this method is not implicitly invoked.
        """ Set the password, with the given algorithms
            param pw is assumed clean and safe, and 
            is validated for length
        """
        if len(pw) < MINIMUM_PASSWORD_LENGTH:
            raise ValidationError("Given password is to short, " \
                                  + "minimum length is %d characters"
                                  % (MINIMUM_PASSWORD_LENGTH));

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    
    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
    
    def get_name_nick(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        if self.nickname:
            full_name = '%s "%s" %s' % (self.first_name, self.nickname, self.last_name)
        else:
            full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def send_activation_email(self, site, url):
        """
        Send an activation email to the user associated with this
        ``RegistrationProfile``.

        The activation email will make use of two templates:

        ``registration/activation_email_subject.txt``
            This template will be used for the subject line of the
            email. Because it is used as the subject line of an email,
            this template's output **must** be only a single line of
            text; output longer than one line will be forcibly joined
            into only a single line.

        ``registration/activation_email.txt``
            This template will be used for the body of the email.

        These templates will each receive the following context
        variables:

        ``activation_key``
            The activation key for the new account.

        ``expiration_days``
            The number of days remaining during which the account may
            be activated.

        ``site``
            An object representing the site on which the user
            registered; depending on whether ``django.contrib.sites``
            is installed, this may be an instance of either
            ``django.contrib.sites.models.Site`` (if the sites
            application is installed) or
            ``django.contrib.sites.models.RequestSite`` (if
            not). Consult the documentation for the Django sites
            framework for details regarding these objects' interfaces.

        """
        ctx_dict = {'activation_key': self.activation_key,
                    'contest':url,
                    'site': site}
        subject = render_to_string('registration/activation_email_subject.txt',
                                   ctx_dict)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())

        message = render_to_string('registration/activation_email_messagebody.txt',
                                   ctx_dict)
        self.email_user(subject, message)

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email]);



    """Swaps in the new email"""
    def activate_new_email(self, key):
        assert self.email_activation_key==key
        self.email = self.temp_email
        self.temp_email = None
        self.email_activation_key = None
        
    def is_on_team(self):
        import pdb
        pdb.set_trace()
        pass
