""" The models used in this app are not intended to be managed - they're used
    to register view functions for the admin interface
"""

from django.db import models
from openshift.contest.models import Team

class string_with_title(str):
    """ Class used to modify the registered URL link TEXT
        in the admin interface
    """
    def __new__(cls, value, title):
        instance = str.__new__(cls, value)
        #pylint:disable=W0212
        instance._title = title
        return instance

    def title(self):
        return self._title

    __copy__ = lambda self: self
    __deepcopy__ = lambda self, memodict: self

class RenderCSV(models.Model):
    latex_text = models.TextField()

class RenderTexOrEmail(models.Model):
    latex_text = models.TextField()
    team = models.ForeignKey(Team)
# EOF
