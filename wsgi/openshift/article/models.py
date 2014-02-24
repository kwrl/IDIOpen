from django.db import models

from django.contrib.auth.models import User
# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    contest = models.ForeignKey('contest.Contest')
    text = models.TextField()
# author = models.ForeignKey(User, null = True, blank = True, editable = False)
# I don't use User as a foreignkey here, so an article isn't directly linked to an User model
    author = models.CharField(max_length=200, null = True, blank = True, editable = False)
    
    def __str__(self):      #Default return string
        return self.title
    
