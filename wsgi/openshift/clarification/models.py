from django.db import models
from contest.models import Team

class Message (models.Model):

    subject = models.TextField()
    body = models.CharField(max_length = 120)
    sender = models.ForeignKey(Team)
    sent_at = models.DateTimeField(null=True, blank=True)
    