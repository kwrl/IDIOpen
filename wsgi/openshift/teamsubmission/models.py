from django.db import models
from django.conf import settings
from django.core.files.storage import Storage

import os

from execution.models import Problem
from contest.models import Team, Contest

def get_upload_path(instance, filename):
    """ Dynamically decide where to upload the case,
        based on the foreign key in instance, which is required to be 
        a Submission.
    """
    # path.join appends a trailing / in between each argument
    return os.path.join("%s" % 'somewhere',
                        "%s/submissions" % (instance.problem),
                        filename);


class MyStorage(Storage):
    def __init__(self, option=None):
        if not option:
            option = settings.CUSTOM_STORAGE_OPTIONS
            
    def delete(self, *args, **kwargs):
        pass

    def exists(self, *args, **kwargs):
        pass

    def listdir(self, *args, **kwargs):
        pass

    def size(self, *args, **kwargs):
        pass

    def url(self, *args, **kwargs):
        return None

class ScoreManager(models.Manager):
    def get_problem_score(self, team, problem):
        """ This constant is the penalty
            for delivering incorrect submissions.
        """
        submission_penalty = 2
        submissions = Submission.objects.filter(team=team).filter(problem=problem).order_by('-date_uploaded')
        correctSubmissions = Submission.objects.filter(team=team).filter(problem=problem).filter(validated=True).order_by('date_uploaded')
        if(len(correctSubmissions) <= 0):
            return 0
        
        timeScore = (correctSubmissions[0].date_uploaded - problem.contest.start_date).total_seconds()
        submissionScore = len(submissions) * submission_penalty
        return timeScore + submissionScore
    
    def get_team_score(self, team, contest):
        problems = Problem.objects.filter(contest=contest)
        score = 0
        for problem in problems:
            score = score + ScoreManager.get_problem_score(self, team, problem)
        return score

class Submission(models.Model):
    submission = models.FileField(upload_to=get_upload_path)
    date_uploaded = models.DateTimeField(auto_now = True)

    validated = models.BooleanField(default=False)
    text_feedback = models.CharField(max_length=50)
    team = models.ForeignKey(Team)
    problem = models.ForeignKey(Problem)   
    objects = ScoreManager()
    
# EOF