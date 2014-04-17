from django.db import models
from contest.models import Team
from userregistration.models import CustomUser
from django.contrib import messages
from django.db.models import signals

def notify_admin(sender, instance, created, **kwargs):
    ''' Notify the administrator that a new message has been added.'''  
    if created:
        # TODO: Notify all admins that a new message has been received
        import ipdb; ipdb.set_trace()    
        
class Message (models.Model):
    subject = models.CharField(max_length = 120)
    body = models.TextField(max_length = 355)
    sender = models.ForeignKey(Team)
    sent_at = models.DateTimeField(null=True, blank=True)
    answered_by = models.ForeignKey(CustomUser, blank = True, null = True)
    answered_at = models.DateTimeField(null=True, blank=True)
    
signals.post_save.connect(notify_admin, sender=Message)
