from django.db import models

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    contest = models.ForeignKey('contest.Contest')
    text = models.TextField()
    
    def __str__(self):      #Default return string
        return self.title
    
