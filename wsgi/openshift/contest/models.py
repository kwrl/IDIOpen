#coding: utf-8

from django.core.exceptions import ValidationError;
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from filebrowser.fields import FileBrowseField


'''
Contest model

TODO: Add location, fix start, end, publish date, validate
'''

from django.db import models
from django.core.urlresolvers import reverse

class Contest(models.Model):
    title = models.CharField(max_length=200)
    """ The url is saved as the suffix from root, only, not the entire url
    """
    url = models.CharField(max_length=20, unique=True);
    start_date = models.DateTimeField(verbose_name='Start date')
    end_date = models.DateTimeField('End date')
    publish_date = models.DateTimeField('Publish date')
    links = models.ManyToManyField('Link')
    css = FileBrowseField('CSS', max_length=200, directory='css/', 
                          extensions=['.css',], blank=True, null=True)

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
    leader = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='leader')
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='members')
    contest = models.ForeignKey(Contest, related_name='contest')
    def __str__(self):
        return self.name
        
# EOF
