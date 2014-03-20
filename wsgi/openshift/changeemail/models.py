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
    def get_instance(self, activation_key):
        SHA1_RE = re.compile('^[a-f0-9]{40}$');
        instance = None;

        if SHA1_RE.search(activation_key):
            try:
                instance = self.get(activation_key=activation_key);
            except self.model.DoesNotExist:
                return None;

            return instance
        else:
            return None;
    

class ChangeEmail(models.Model):
    """
    A model to temporarily store an email adress change request.

    USAGE:
        #1 invoke the model as an instance,
        #2 invoke model.save() with user, new email
        #3 invoke model.send_confirmation_mail(request) (request for emails)

        --
        #1 When the user accesses the url in the email, he will be directed to
             a view. From the view, invoke model.get(activation_key...)
        #2 invoke updateUser, which will delete $THIS and update the email.
    """        
    new_email = models.EmailField(unique=False);
    created_date = models.DateTimeField(auto_now_add=True, unique=False);
    refuser = models.ForeignKey(settings.AUTH_USER_MODEL, 
            related_name='contestant', null = False,
            );
    activation_key = models.CharField(max_length=40, null=False, unique=True);

    objects = ChangeEmailManager();

    class Meta:
        verbose_name = _('email address change request');
        verbose_name_plural = _('email address change requests');
        
    def __make_activation_key(self):
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5];
        return hashlib.sha1(salt+self.refuser.email.encode('utf-8')).hexdigest();    

    def save(self, user, new_email, *args, **kwargs):
        self.refuser = user;
        self.new_email = new_email;
        self.activation_key = self.__make_activation_key();
        super(ChangeEmail, self).save(*args, **kwargs);

    def updateUser(self):
        self.refuser.email = self.new_email;
        self.refuser.save();
        #TODO: should there be a post-save signal here? See django-docs.
        #    : this is to verify that the user email is actually updated.


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
                    'user':self.refuser.get_full_name(),
                    'date': self.created_date,
                    'site': site,
                    };
        subject = render_to_string('changeEmail/change_email_subject.txt', ctx_dict)
        # ubject = ''.join(subject.splitlines())
        content = render_to_string('changeEmail/change_email_content.txt', ctx_dict)
        print content;
        send_mail(subject, content, '', [self.new_email]);
        
# EOF        
