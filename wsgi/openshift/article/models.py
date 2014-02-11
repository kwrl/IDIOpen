from openshift.article import models
from openshift.article import Contest

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    contest = models.ForeignKey('Contest')
    text = models.TextField()
    
    def __str__(self):      #Default return string
        return self.title
    
