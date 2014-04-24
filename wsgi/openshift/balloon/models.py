from django.db import models

from openshift.contest.models import Team, Contest
from openshift.teamsubmission.models import Submission, Problem

class BalloonStatus(models.Model):
    """ Model
    """
    timestamp = models.DateTimeField()
    """ Whether a balloon has actually been given to the team or not
    """
    submission = models.ForeignKey(Submission)
    problem = models.ForeignKey(Problem)
    team = models.ForeignKey(Team)

class string_with_title(str):
    def __new__(cls, value, title):
        instance = str.__new__(cls, value)
        instance._title = title
        return instance

    def title(self):
        return self._title

    __copy__ = lambda self: self
    __deepcopy__ = lambda self, memodict: self


class balloon_view(models.Model):
    class Meta:
        managed = True 
        verbose_name = "Click here to view balloon table"
        verbose_name_plural = "Click here to view balloon table"
    
# EOL