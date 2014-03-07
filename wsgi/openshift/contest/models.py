from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from filebrowser.fields import FileBrowseField
from django.forms import ModelForm
from django import forms
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist

# Create your models here.

User = get_user_model()
'''
Contest model

TODO: Add location, fix start, end, publish date, validate
'''
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

# Links for displaying in navigation for each contest    
class Link(models.Model):
    #name of the link
    text = models.CharField(max_length=30)
    # If true, url gets added to contest url
    # eg. url is 'article/1' if true gives '/open14/article/1'
    contestUrl = models.BooleanField()
    url = models.CharField(max_length=50)

    def __str__(self):
        return self.text


 
    
class Team(models.Model):
    name = models.CharField(max_length=200)
    onsite = models.BooleanField()
    '''
    TODO: Set leader 
    NOTE: in order to implement leader we information about the logged in user. 
    '''
    #leader = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='leader')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='members')
    #contest = models.ForeignKey(Contest, related_name='contest')
    offsite = models.CharField(max_length=200, blank = True)
    def __str__(self):
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



