from django.db import models
from contest.models import Team, Contest
from userregistration.models import CustomUser
from django.conf import settings
    
class Message (models.Model):
    subject     = models.CharField(max_length = 120)
    body        = models.TextField(max_length = 355)
    sender      = models.ForeignKey(Team)    
    sent_at     = models.DateTimeField(null=True, blank=True, auto_now = True)
    contest     = models.ForeignKey(Contest)
    answered    = models.BooleanField(default = False)

class MessageAnswer(models.Model):
    subject     = models.CharField(max_length = 120)
    body        = models.TextField(max_length = 355)
    answered_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank = True, null=True) 
    answered_at = models.DateTimeField(null=True, blank=True, auto_now = True)  
    message     = models.ForeignKey(Message, null=True, blank=True, default = None)
    contest     = models.ForeignKey(Contest)
