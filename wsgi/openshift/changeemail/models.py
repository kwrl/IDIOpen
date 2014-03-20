""" Change the email for a given user. 
    The model defined in this class stores the old user, new email 
    and activation key.

    The manager is to access the entires in a safe and defined manner..

    The functionality has been put in as it's own package so that the feature
    can easily be removed, disabled and to keep the code-base clean.
"""

from django.db import models
from django.conf import settings
from django.contrib.sites.models import RequestSite
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from contest.models import Invite
from userregistration.models import CustomUser as User

import hashlib
import re
import random

class ChangeEmailManager(models.Manager):
    """ Access to ChangeEmail in a safe manner
    """
    def get_instance(self, user, activation_key):
        """ Get the given instance (should be unique under activation_key).
        The user lookup is excessive but provided to avoid errors in use

        @return is either None or a valid instance.
        """
        SHA1_RE = re.compile('^[a-f0-9]{40}$')
        instance = None # default

        if SHA1_RE.search(activation_key):
            try:
                instance = self.get(refuser=user, activation_key=activation_key)
            except self.model.DoesNotExist:
                return None

            return instance
        else:
            return None

    def get_duplicates(self, sug_new_email, activation_key):
        """ Get all instances of new_email, as in self.get_instance, just
            with email instead of user-lookup
        """
        SHA1_RE = re.compile('^[a-f0-9]{40}$')
        if SHA1_RE.search(activation_key):
            return self.filter(new_email=sug_new_email) \
                               .exclude(activation_key=activation_key)
    

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
    new_email = models.EmailField(unique=False)
    created_date = models.DateTimeField(auto_now_add=True, unique=False)
    refuser = models.ForeignKey(settings.AUTH_USER_MODEL, 
            related_name='contestant', null = False,
            )
    activation_key = models.CharField(max_length=40, null=False, unique=True)

    objects = ChangeEmailManager()

    class Meta:
        verbose_name = _('email address change request')
        verbose_name_plural = _('email address change requests')
        
    def __make_activation_key(self):
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        return hashlib.sha1(salt+self.refuser.email.encode('utf-8')).hexdigest()    

    def save(self, user, new_email, *args, **kwargs):
        self.refuser = user
        self.new_email = new_email
        self.activation_key = self.__make_activation_key()
        super(ChangeEmail, self).save(*args, **kwargs)

    def updateUser(self):
        #TODO: should there be a post-save signal here? See django-docs.
        #    : this is to verify that the user email is actually updated 
        #    : and saved before moving on.
        old_email = self.refuser.email
        self.refuser.email = self.new_email
        self.refuser.save()

        assert (self.refuser.email != old_email)

        self.__updateInvites(old_email)
        self.__removeDuplicates()


    def __updateInvites(self, user):
        """ Verify that all updates reflect the email-change of the user
            
            Should be invoked only after updating the user!
        """
        for invite in Invite.objects.filter(email=old_email):
            invite.email = self.new_email
            invite.save()

    def __removeDuplicates(self):
        """ For the (odd) scenario:
                User A and B asks to change to email c.
                User A activates his email change first
                B's request is deleted
        """
        for old_entry in ChangeEmail.objects.get_duplicates(self.new_email,
                                                          self.activation_key):
            old_entry.delete()

    def send_confirmation_mail(self, request):
        """ Send a letter to the user, asking to activate the new email
        """

        # Get the contest
        try: 
            url = request.path.split('/')[1]
        except ObjectDoesNotExist as e: 
            raise error
        
        site = RequestSite(request)
        ctx_dict = {'activation_key': self.activation_key,
                    'contest':url,
                    'new_email': self.new_email,
                    'user':self.refuser.get_full_name(),
                    'date': self.created_date,
                    'site': site,
                    }
        subject = render_to_string('changeEmail/change_email_subject.txt',
                                   ctx_dict)
        content = render_to_string('changeEmail/change_email_content.txt',
                                   ctx_dict)
        send_mail(subject, content, '', [self.new_email])
        
# EOF        
