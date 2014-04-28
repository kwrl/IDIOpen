from django.db import models
from openshift.contest.models import Team

class Latex_Teamview(models.Model):
    latex_text = models.TextField()

class Latex_TeamText(models.Model):
    latex_text = models.TextField()
    team = models.ForeignKey(Team)
# EOF
