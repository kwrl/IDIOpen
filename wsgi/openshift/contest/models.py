from openshift.contest import models

# Create your models here.

class Contest(models.Model):
    title = models.CharField(max_length=200)
    
    start_date = models.DateTimeField('Start date')
    end_date = models.DateTimeField('End date')
    publish_date = models.DateTimeField('Publish date')
    
    
    def __str__(self):
        return self.title