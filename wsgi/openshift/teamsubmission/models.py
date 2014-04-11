from django.db import models

from django.conf import settings
from django.core.files.storage import Storage

import os

from execution.models import Problem
from contest.models import Team, Contest
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

class ScoreManager(models.Manager):
    def get_problem_score(self, team, problem, contest):
        """ 
        This constant is the penalty
        for delivering incorrect submissions.
        """
        submission_penalty = contest.penalty_constant
        submissions = Submission.objects.filter(team=team).filter(problem=problem).order_by('-date_uploaded')
        correctSubmissions = Submission.objects.filter(team=team).filter(problem=problem).filter(solved_problem=True).order_by('date_uploaded')
        if(len(correctSubmissions) <= 0):
            return 0
        timeScore = (correctSubmissions[0].date_uploaded - problem.contest.start_date).total_seconds()
        submissionScore = len(submissions) * submission_penalty
        return timeScore + submissionScore
    
    def get_team_score(self, team, contest):
        problems = Problem.objects.filter(contest=contest)
        score = 0
        for problem in problems:
            score = score + ScoreManager.get_problem_score(self, team, problem, contest)
        return score
    
    def get_highscore(self, contest):
        teams = Team.objects.filter(contest=contest)
        scores = []
        zeros = []
        for team in teams:
            if(ScoreManager.get_team_score(self, team, contest)):
                scores.append((team.name, ScoreManager.get_team_score(self, team, contest)))
            else:
                zeros.append((team.name, ScoreManager.get_team_score(self, team, contest)))
        sorted(scores, key=lambda score: score[1])
        for s in zeros:
            scores.append(s)
        return scores

class Submission(models.Model):
    #We shoul rename submission field.... 
    submission = models.FileField(storage=private_media, upload_to='submissions')
    date_uploaded = models.DateTimeField(auto_now = True)
    solved_problem = models.BooleanField(default=False) #E.g. Did this submission solve the the problem
    text_feedback = models.CharField(max_length=50)
    team = models.ForeignKey(Team)
    problem = models.ForeignKey(Problem)
    runtime = models.IntegerField(max_length = 15, blank = True, null = True)  
    objects = ScoreManager()
    
# EOF