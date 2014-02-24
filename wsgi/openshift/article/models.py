from django.db import models
from django.contrib.auth.models import User 


# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add = True)
    contest = models.ForeignKey('contest.Contest')
    text = models.TextField()
    author = models.ForeignKey(User, null = True, blank = True)
    
    
    def __str__(self):      #Default return string
        return self.title
    
