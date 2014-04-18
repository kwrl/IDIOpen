from django.db import models
from contest.models import Team, Contest
from userregistration.models import CustomUser

#def notify_admin(sender, instance, created, **kwargs):
#    ''' Notify the administrator that a new message has been added.'''  
#    if created:
        # TODO: Notify all admins that a new message has been received
#        pass
    
class Message (models.Model):
    subject     = models.CharField(max_length = 120)
    body        = models.TextField(max_length = 355)
    sender      = models.ForeignKey(Team)    
    sent_at     = models.DateTimeField(null=True, blank=True, auto_now = True)
    contest     = models.ForeignKey(Contest)

class MessageAnswer(models.Model):
    subject     = models.CharField(max_length = 120, default='Not Yet Answered')
    body        = models.TextField(max_length = 355, default='Not Yet Answered')
    answered_by = models.ForeignKey(CustomUser, blank = True, null=True) 
    answered_at = models.DateTimeField(null=True, blank=True, auto_now = True)  
    message     = models.ForeignKey(Message)
    contest     = models.ForeignKey(Contest)
      
#signals.post_save.connect(notify_admin, sender=Message)
