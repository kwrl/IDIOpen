from django.db import models
from openshift.contest.models import Team

class FakeTeam(object):
    #objects = Team.objects
    team = models.ForeignKey(Team, related_name="aa")
    pass

class string_with_title(str):
    def __new__(cls, value, title):
        instance = str.__new__(cls, value)
        #pylint:disable=W0212
        instance._title = title
        return instance

    def title(self):
        return self._title

    __copy__ = lambda self: self
    __deepcopy__ = lambda self, memodict: self

class Latex_Teamview(models.Model):
    latex_text = models.TextField()

class Latex_TeamText(models.Model):
    latex_text = models.TextField()
    team = models.ForeignKey(Team)
# EOF
