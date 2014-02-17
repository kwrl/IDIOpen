from django.db import models
from datetime import datetime
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
import django.contrib.auth
from django.contrib.auth import get_user_model
from django.conf import settings
from filebrowser.fields import FileBrowseField
# Create your models here.

class CustomUserManager(BaseUserManager):

    def _create_user(self, email, name, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          name=name,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, name, password=None, **extra_fields):
        return self._create_user(email, name, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, name, password, **extra_fields):
        return self._create_user(email, name, password, True, True,
                                 **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    A fully featured User model with admin-compliant permissions that uses
    a full-length email field as the username.

    Email and password are required. Other fields are optional.
    """
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    name = models.CharField(_('name'), max_length=30, blank=False)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name',]

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        return self.name

    def get_short_name(self):
        "Returns the short name for the user."
        return self.name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

class Contest(models.Model):
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=20, unique=True)
    start_date = models.DateTimeField('Start date')
    end_date = models.DateTimeField('End date')
    publish_date = models.DateTimeField('Publish date')
    links = models.ManyToManyField('Link')
    css = FileBrowseField('CSS', max_length=200, directory='css/', extensions=['.css',], blank=True, null=True)
    
    
    def __str__(self):
        return self.title
    
class Link(models.Model):
    text = models.CharField(max_length=30)
    contestUrl = models.BooleanField()
    url = models.CharField(max_length=50)
    
    def __str__(self):
        return self.text
    

class Contestant(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=200)
    nickName = models.CharField(max_length=200)
    dateJoined = datetime.now()
    
    def __str__(self):
        return self.name
    
class Team(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    onsite = models.BooleanField()
    leader = models.ForeignKey(Contestant, related_name='leader')
    members = models.ManyToManyField(Contestant, related_name='members')
    contest = models.ForeignKey(Contest, related_name='contest')
    def __str__(self):
        return self.user.name
        