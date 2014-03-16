from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    contest = models.ForeignKey('contest.Contest')
    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null = True, blank = True, editable = False)
# I don't use User as a foreignkey here, so an article isn't directly linked to an User model
    #author = models.CharField(max_length=200, null = True, blank = True, editable = False)
    visible_article_list = models.BooleanField(default=True, help_text = 
                           'If this is set the article will appear in the article list, defaults to True')
    url = models.CharField(null = True, blank = True, max_length=200, unique=True,
                           help_text = 'Set the url to access this page \'/pages/[url]/\'' )
    
    def __unicode__(self):      #Default return string
        return self.title
    
