from django.db import models
from openshift.contest.models import Team, Contest
from django.conf import settings
    
class Question (models.Model):
    
    class Meta:
        verbose_name = "or add an answer to a question"
        verbose_name_plural = "Click here to view and answer questions"
    subject     = models.CharField(max_length = 120)
    body        = models.TextField(max_length = 355)
    sender      = models.ForeignKey(Team)    
    sent_at     = models.DateTimeField(null=True, blank=True, auto_now = True)
    contest     = models.ForeignKey(Contest)
    answered    = models.BooleanField(default = False, 
                    help_text='Uncheck this if you think the question hasn\'t been answered. \
                     This checkbox will be automatically checked when an answer has been provided to the question.')

    def __unicode__(self):
        return self.subject

class QuestionAnswer(models.Model):

    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Click here to view answers"
   
    subject     = models.CharField(max_length = 120)
    body        = models.TextField(max_length = 355)
    answered_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank = True, null=True) 
    answered_at = models.DateTimeField(null=True, blank=True, auto_now = True)  
    question    = models.ForeignKey(Question, null=True, blank=True, default = None)
    contest     = models.ForeignKey(Contest)
