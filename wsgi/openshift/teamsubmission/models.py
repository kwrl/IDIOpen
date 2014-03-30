from django.db import models

import os

from execution.models import Problem
from contest.models import Team

def get_upload_path(instance, filename):
    """ Dynamically decide where to upload the case,
        based on the foreign key in instance, which is required to be 
        a Submission.
    """
    # path.join appends a trailing / in between each argument
    return os.path.join("%s" % 'somewhere',
                        "%s/case" % (instance.problem),
                        filename);

class Submission(models.Model):
    team = models.ForeignKey(Team)
    problem = models.ForeignKey(Problem)
    
    submission = models.FileField(upload_to=get_upload_path)
    date_uploaded = models.DateTimeField()
    
    validated = models.BooleanField()
    text_feedback = models.CharField(max_length=50)


# EOF