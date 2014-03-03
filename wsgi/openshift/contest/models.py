from django.db import models
from django.contrib.auth.models import User
from filebrowser.fields import FileBrowseField
from django.forms import ModelForm
from django import forms; 

# Create your models here.


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
    team_name = models.CharField(max_length=200)
    onsite = models.BooleanField()
    offsite = models.CharField(max_length= 100)
    #leader = models.ForeignKey(User, related_name='leader')
    members = models.ManyToManyField(User, related_name='members')
    #contest = models.ForeignKey(Contest, related_name='contest')
    
    def __str__(self):
        return self.name
        
        


    
    