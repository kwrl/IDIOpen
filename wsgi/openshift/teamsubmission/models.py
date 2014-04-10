from django.db import models

from django.conf import settings
from django.core.files.storage import Storage

import os

from openshift.execution.models import Problem
from openshift.contest.models import Team
from django.core.files.storage import FileSystemStorage

private_media = FileSystemStorage(location=settings.PRIVATE_MEDIA_ROOT,
                                  base_url=settings.PRIVATE_MEDIA_URL,
                                  )

def get_upload_path(instance, filename):
    """ Dynamically decide where to upload the case,
        based on the foreign key in instance, which is required to be 
        a Submission.
    """
    # path.join appends a trailing / in between each argument
    return os.path.join("%s" % 'somewhere',
                        "%s/submissions" % (instance.problem),
                        filename);

class Submission(models.Model):
    submission = models.FileField(storage=private_media, upload_to='submissions')
    date_uploaded = models.DateTimeField(auto_now = True)
    solved_problem = models.BooleanField(default=False) #E.g. Did this submission solve the the problem
    text_feedback = models.CharField(max_length=50)
    team = models.ForeignKey(Team)
    problem = models.ForeignKey(Problem)
    runtime = models.IntegerField(max_length = 15, blank = True, null = True)  
    
# EOF
