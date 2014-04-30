#coding: utf-8
from openshift.userregistration.models import CustomUser as User 
from sortedm2m.fields import SortedManyToManyField
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from filebrowser.fields import FileBrowseField
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from openshift.userregistration.models import CustomUser as User
import datetime
from django.utils import timezone

# Create your models here.




def getTodayDate():
    return timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())

class ContactInformation(models.Model):
    '''
    Simple entity for storing contact information. Initially only used in the website footer
    for adding support info.
    '''
    email = models.EmailField()
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name


def is_start():
    return False

class Contest(models.Model):
    '''
	This class represents a contest. Every article, submission, team etc are in some way related to
	an instance of this class. Other than binding the other entities together it sets the start
	date for the contest, the end date, a registration end date, and a publish date. The penalty 
	constant used to calculate team scores is also set in this model.
    '''
    title = models.CharField(max_length=200)
    contact_infos = models.ManyToManyField('ContactInformation', null = True)
    """ The url is saved as the suffix from root, only, not the entire url
    """

    penalty_constant = models.IntegerField('Penalty Constant', default = 0)
    url = models.CharField(max_length=20, unique=True, help_text='Defines the url used to access the contest. E.g. sample.site.com/[the value inserted here]');
    start_date = models.DateTimeField(verbose_name='Start date');
    end_date = models.DateTimeField('End date');
    publish_date = models.DateTimeField('Publish date');
    teamreg_end_date = models.DateTimeField("Team registration close date");
    links = SortedManyToManyField('Link');
    sponsors = models.ManyToManyField('Sponsor', blank=True)
    css = FileBrowseField('CSS', max_length=200, directory='css/',
                          extensions=['.css',], blank=True, null=True)
    logo = FileBrowseField('Logo', max_length=200, directory='logo/', 
                          extensions=['.jpg','.jpeg','.png','.gif'], blank=True, null=True,
                          help_text='Select logo image, allowed formats jpg, jpeg, png, gif')
    
    problem_set = PrivateFileField("file", upload_to = 'problemset', condition = is_start)

    def isPublishable(self):
        return self.publish_date.__lt__(getTodayDate())

    def isRegOpen(self):
        return self.teamreg_end_date.__gt__(getTodayDate())

    def clean(self):
        # TODO: which is better? To do clean here, or in form?
        # in model you can only invoke validationerror on _ALL_ fields,
        # not a single one
        if self.start_date is not None and self.end_date is not None:
            if self.start_date.__lt__(self.end_date) == False:
                raise ValidationError('You cannot set start date to be after the end date')
            
    def __str__(self):
        return self.title



    
# Links for displaying in navigation for each contest    
class Link(models.Model):
    '''
	Used to dynamically add links to the global left side menu on the website.
	Can also be used to create empty space between other links, in which case
	it is called a separator. 
    '''
    #name of the link
    text = models.CharField(max_length=30, help_text='The display name for the link')
    # If true, url gets added to contest url
    # eg. url is 'article/1' if true gives '/open14/article/1'
    # contestUrl = models.BooleanField(help_text='Contest URLs are extensions of the contest root URL. '             'Example: \'/idiopen14/accounts/register/\'')
    contestUrl = models.BooleanField(verbose_name='Is this a link from this website?',
                                     help_text=
    'If this is a link from this website, the {contest-url} will be put at the root of the URL for you.'+
    'E.g.: /idiopen14/accounts/register/{your new article/url}')
    url = models.CharField(max_length=50, 
                           help_text=' Internal links need leading and trailing slashes.'+
                           ' External links are required to start with "http://"')

    separator = models.BooleanField(help_text = 'Seperator is for creating \"whitespace\" in the left-hand link menu.'
                                    )
    def __unicode__(self):
        return self.text

    
 
    
class Team(models.Model):
    '''
	Used to represent a team competing in a specific contest. A team consists of
	a group of users, the team members, one of which is set to be the team leader.
	Team members can choose to leave a team, but other than that only the team
	leader can edit the team. 
	'''
    name = models.CharField(max_length=50, verbose_name = "Team name")
    onsite = models.BooleanField()
    leader = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='leader', null = True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='members')
    contest = models.ForeignKey('Contest', related_name='contest', null=True)
    offsite = models.CharField(max_length=30, blank = True, verbose_name = "Offsite Location")

    def __unicode__(self):
        return self.name
    
    #===============================================================================
    # Removes trailing whitespace from all CharFields and TextFields in Team Model
    # 
    # Note: For some reason this only works for Team_Edit form and not for Team_Form
    #===============================================================================
    def clean(self):
        for field in self._meta.fields:
            if isinstance(field, (models.CharField, models.TextField)):
                value = getattr(self, field.name)
                if value:
                    setattr(self, field.name, value.strip())
                                      
class InviteManager(models.Manager):
	'''
	Used to handle invites. If a team leader invites a new user to his team
	the create_invite function is called and an invite instance is created.
	Finally the send_new_mail is called to notify the user of the invite.
	'''
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

        send_mail(subject, message, False, [email,])
        

class Invite(models.Model):
	'''
	Represents an invitation to join a team in the database.
	'''
    email = models.EmailField() 
    team = models.ForeignKey('Team')
    is_member = models.BooleanField(default=False)
    objects = InviteManager()
    
    def __unicode__(self):
        return self.team.name + ' ' + self.email


class Sponsor(models.Model):
	'''
	Sponsors need ad space. Logos etc are stored as instances of this class and displayed on the website.
	'''
    name = models.CharField(max_length=50, default='Logo', help_text='Company name for the sponsor')
    url = models.URLField(help_text='The url you want the user to get redirected to when the logo is clicked')  
    image = FileBrowseField('Image', max_length=200, directory='sponsor/', 
                          extensions=['.jpg','.jpeg','.png','.gif'], blank=False, null=False,
                          help_text='Select logo image, allowed formats jpg, jpeg, png, gif')
    
    def __unicode__(self):
        return self.name
     

# EOF
