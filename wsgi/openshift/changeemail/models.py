import hashlib
import random

from django.core.exceptions import ObjectDoesNotExist;
from django.core.mail import send_mail;
from django.db import models;
from django.template.loader import render_to_string;
from django.utils.translation import ugettext_lazy as _;
from django.utils import timezone;
from django.contrib.sites.models import RequestSite
from django.core.mail import send_mail

from django.db import models;

from userregistration.models import CustomUser as User;

from django.conf import settings;

import re;

class ChangeEmailManager(models.Manager):
    def activate_email(self, activation_key):
            SHA1_RE = re.compile('^[a-f0-9]{40}$');
            if SHA1_RE.search(activation_key):
                try:
                    #import ipdb; ipdb.set_trace();

                    #instance = self.values()[0]['user']
                    user = self.get(activation_key=activation_key)
                    #instance = self.get(activation_key=activation_key);
                    #user = User.objects.get(pk=self.values()[0]['user_id'])
                except self.model.DoesNotExist:
                    return False
                #user.activation_key = self.model.ACTIVATED
                #self.save()
                return instance
            return False
        
    
class ChangeEmail(models.Model):
    """
    A model to temporarily store an email adress change request.
    """        
    new_email = models.EmailField();
    created_date = models.DateTimeField(auto_now_add=True);
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='contestant', null = True);
    activation_key = models.CharField(max_length=40, null=False, unique=True);
    #objects = ChangeEmailManager();

    class Meta:
        verbose_name = _('email address change request');
        verbose_name_plural = _('email address change requests');
        
    def __init__(self, user, new_email, *args, **kwargs):
        super(ChangeEmail, self).__init__(*args, **kwargs);
        self.user = user;
        self.new_email = new_email;
        
    def __unicode__(self):
        return "%s" % self.user;

    def has_expired(self, seconds=None):
        pass;

    def get_expiration_date(self, seconds=None):
        pass;
    
    def activate_mail(self, activation_key):
        SHA1_RE = re.compile('^[a-f0-9]{40}$')
        if SHA1_RE.search(activation_key):
            try:
                ce = self.get(activation_key=activation_key);
                user = User.objects.get(pk=ce.User)
                print user
                user.email = ce.new_email
            except self.model.DoesNotExist:
                return False;
            user.is_active = True;
            user.activation_key = self.model.ACTIVATED;
            user.save();
            return user;

    def make_activation_key(self):
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5];
        self.activation_key = hashlib.sha1(salt+self.user.email.encode('utf-8')).hexdigest();    

    def send_confirmation_mail(self, request):
        try: 
            url = request.path.split('/')[1]
        except ObjectDoesNotExist as e: 
            raise error;
        
        site = RequestSite(request)
        print site
        
        ctx_dict = {'activation_key': self.activation_key,
                    'contest':url,
                    'new_email': self.new_email,
                    'user':self.user.get_full_name(),
                    'date': self.created_date,
                    'site': site,
                    };
        subject = render_to_string('changeEmail/change_email_subject.txt', ctx_dict)
        # ubject = ''.join(subject.splitlines())
        content = render_to_string('changeEmail/change_email_content.txt', ctx_dict)
        print content;
        send_mail(subject, content, 'penis', [self.new_email]);


    def activate_email(self, activation_key):
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
            SHA1_RE = re.compile('^[a-f0-9]{40}$');
            user = None;
            if SHA1_RE.search(activation_key):
                try:
                    print ChangeEmail.objects.get(activation_key=activation_key)
                    ce = ChangeEmail.objects.get(activation_key=activation_key)
                    user = User.objects.get(pk=ce.User)
                    print user
                    user.email = ce.new_email
                except self.DoesNotExist:
                    return False;
                user.is_active = True;
                user.activation_key = self.model.ACTIVATED;
                user.save();
            return user;
        
# EOF        