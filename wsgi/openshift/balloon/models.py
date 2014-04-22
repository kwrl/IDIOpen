from django.db import models

from openshift.contest.models import Team, Contest
from openshift.teamsubmission.models import Submission, Problem

class BalloonStatus(models.Model):
    """ Model
    """
    timestamp = models.DateTimeField()
    """ Whether a ballon has actually been given to the team or not
    """
    submission = models.ForeignKey(Submission)
    problem = models.ForeignKey(Problem)
    team = models.ForeignKey(Team)
    
# EOL