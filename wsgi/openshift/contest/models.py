#coding: utf-8

from sortedm2m.fields import SortedManyToManyField
from django.core.exceptions import ValidationError;
from django.db import models
from django.contrib.auth import get_user_model;
from django.conf import settings;
from filebrowser.fields import FileBrowseField;
from django.forms import ModelForm;
from django import forms;
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist

import datetime;
from django.utils import timezone;

# Create your models here.

User = get_user_model()
'''
Contest model

TODO: Add location, fix start, end, publish date, validate
'''

from django.db import models
from django.core.urlresolvers import reverse

def getTodayDate():
     return timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone());

class ContactInformation(models.Model):
    email = models.EmailField()
    phone = models.IntegerField(max_length=12)

class Contest(models.Model):
    title = models.CharField(max_length=200)
    contact_infos = models.ManyToManyField(ContactInformation)
    """ The url is saved as the suffix from root, only, not the entire url
    """
    url = models.CharField(max_length=20, unique=True);
    start_date = models.DateTimeField(verbose_name='Start date');
    end_date = models.DateTimeField('End date');
    publish_date = models.DateTimeField('Publish date');
    teamreg_end_date = models.DateTimeField("Team registration close date");
    links = SortedManyToManyField('Link');
    sponsors = models.ManyToManyField('Sponsor', blank=True)
    css = FileBrowseField('CSS', max_length=200, directory='css/',
                          extensions=['.css',], blank=True, null=True)

    def isPublishable(self):
        return self.publish_date.__lt__(getTodayDate());

    def isRegOpen(self):
        return self.teamreg_end_date.__gt__(getTodayDate());

    def clean(self):
        # TODO: which is better? To do clean here, or in form?
        # in model you can only invoke validationerror on _ALL_ fields,
        # not a single one
        if self.start_date is not None and self.end_date is not None:
            if self.start_date.__lt__(self.end_date) == False:
                raise ValidationError('You cannot set start date to be after the end date');
            
    def __str__(self):
        return self.title
    
    
        
    
     
# Links for displaying in navigation for each contest    
class Link(models.Model):
    #name of the link
    text = models.CharField(max_length=30, help_text='The display name for the link')
    # If true, url gets added to contest url
    # eg. url is 'article/1' if true gives '/open14/article/1'
    contestUrl = models.BooleanField(help_text='If the url requires the contest url as prefix,' +
                                     'example \'/open14/accounts/register/\'')
    url = models.CharField(max_length=50, 
                           help_text='Example \'/accounts/register/\','+
                           ' make sure to have leading and trailing slashes.'+
                           ' The url can also link to external web pages')

    def __unicode__(self):
        return self.text


 
    
class Team(models.Model):
    name = models.CharField(max_length=200, verbose_name = "Team name")
    onsite = models.BooleanField()
    '''
    TODO: Set leader 
    NOTE: in order to implement leader we information about the logged in user. 
    '''
    leader = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='leader', null = True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='members')
    contest = models.ForeignKey(Contest, related_name='contest', null=True)
    offsite = models.CharField(max_length=200, blank = True)
    def __unicode__(self):
        return self.name

        
class InviteManager(models.Manager):
    def create_invite(self, email, team, url, site):
        invite = self.create(email=email, team=team)
        user = User.objects.filter(email=email)
        
        try:
            user = User.objects.get(email=email)
            self.send_new_mail(user.email, url, site, True)
        except ObjectDoesNotExist:
            self.send_new_mail(email, url, site, False)
            
        return invite
        
    def send_new_mail(self, email, url, site, registered):
        ctx_dict = {'contest':url,
                    'site': site}
        subject = render_to_string('registration/team_register_email_subject.txt',
                                   ctx_dict)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        
        if registered:
            message = render_to_string('registration/team_join_email.txt', ctx_dict)
        else:
            message = render_to_string('registration/team_register_email.txt', ctx_dict)

        # send_mail(subject, message, False, [email,])
        

class Invite(models.Model):
    email = models.EmailField(); 
    team = models.ForeignKey(Team)
    is_member = models.BooleanField(default=False);
    objects = InviteManager()
    
    def __unicode__(self):
        return self.team.name + ' ' + self.email


class Sponsor(models.Model):
    name = models.CharField(max_length=50, default='Logo', help_text='Company name for the sponsor')
    url = models.URLField(help_text='The url you want the user to get redirected to when the logo is clicked')  
    image = FileBrowseField('Image', max_length=200, directory='sponsor/', 
                          extensions=['.jpg','.jpeg','.png','.gif'], blank=False, null=False,
                          help_text='Select logo image, allowed formats jpg, jpeg, png, gif')
    
    def __unicode__(self):
        return self.name
     

# EOF
