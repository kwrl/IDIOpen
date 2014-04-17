from django.db import models
from contest.models import Team, Contest
from userregistration.models import CustomUser

class Message (models.Model):

    subject = models.CharField(max_length = 120)
    body = models.TextField(max_length = 355)
    sender = models.ForeignKey(Team)
    sent_at = models.DateTimeField(null=True, blank=True, auto_now = True)
    answared_by = models.ForeignKey(CustomUser, blank = True, null=True)
    answared_at = models.DateTimeField(null=True, blank=True)
    contest = models.ForeignKey(Contest)
        
    