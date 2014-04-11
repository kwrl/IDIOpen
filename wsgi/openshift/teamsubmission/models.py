from django.db import models

from django.conf import settings
from django.core.files.storage import Storage

import os

from execution.models import Problem
from contest.models import Team, Contest
from django.core.files.storage import FileSystemStorage

import operator

private_media = FileSystemStorage(location=settings.PRIVATE_MEDIA_ROOT,
                                  base_url=settings.PRIVATE_MEDIA_URL,
                                  )

def get_upload_path(instance, filename):
    """ 
    Dynamically decide where to upload the case,
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
        submissions = Submission.objects.filter(team=team).filter(problem=problem).filter(solved_problem=False).order_by('-date_uploaded')
        correctSubmissions = Submission.objects.filter(team=team).filter(problem=problem).filter(solved_problem=True).order_by('date_uploaded')

        """ 
        The statistics are:
        [total score,
        time submitted (in minutes),
        submission score,
        number of submissions]
        """
        statistics = [0, 0, 0, len(submissions)]
        if(len(correctSubmissions) > 0):
            time = int((correctSubmissions[0].date_uploaded - problem.contest.start_date).total_seconds()) / 60
            submissionScore = len(submissions) * submission_penalty
            
            statistics[0] = time + submissionScore
            statistics[1] = time
            statistics[2] = submissionScore
            statistics[3] = len(submissions) + 1
        
        return statistics    
    
    def get_team_score(self, team, contest):
        problems = Problem.objects.filter(contest=contest)
        
        """ 
        The statistics are:
        [solved problems,
        total score,
        time submitted (in minutes),
        problem 1 submissions/time solved,
        ...
        problem n submissions/time solved]
        """
        statistics = [0, 0, 0]
        for problem in problems:
            problemStat = ScoreManager.get_problem_score(self, team, problem, contest)
            if problemStat[0]:
                statistics[0] = statistics[0] + 1
            statistics[1] = statistics[1] + problemStat[0]
            statistics[2] = statistics[2] + problemStat[1]
            if(problemStat[1]):
                statistics.append(str(problemStat[3]) + "/" + str(problemStat[1]))
            else:
                statistics.append(str(problemStat[3]) + "/--")
        return statistics
    
    def get_highscore(self, contest):
        teams = Team.objects.filter(contest=contest)
        
        """ 
        The statistics are:
        [position,
        team name,
        solved problems,
        total score,
        total time (in minutes),
        problem 1 submissions,
        ...
        problem n submissions,]
        """
        statistics = []
        
        """ 
        zeros is a list of teams that have 0 in total score. These teams haven't
        solved any problems, and should be at the bottom of the scoreboard.
        """
        zeros = []
        for team in teams:
            teamStats = ScoreManager.get_team_score(self, team, contest)
            highscore = [0, team.name]
            if(teamStats[0]):
                for field in teamStats:
                    highscore.append(field)
                statistics.append(highscore)
            else:
                teamStats[0] = ""
                for field in teamStats:
                    highscore.append(field)
                zeros.append(highscore)
        statistics = sorted(statistics, key=lambda x : (-x[2], x[3]))
        for i in range(len(statistics)):
            statistics[i][0] = i + 1
        
        for s in zeros:
            s[0] = len(statistics) + 1
            statistics.append(s)
        return statistics

class Submission(models.Model):
    #We should rename submission field.... 
    submission = models.FileField(storage=private_media, upload_to='submissions')
    date_uploaded = models.DateTimeField(auto_now = True)
    solved_problem = models.BooleanField(default=False) #E.g. Did this submission solve the the problem
    text_feedback = models.CharField(max_length=50)
    team = models.ForeignKey(Team)
    problem = models.ForeignKey(Problem)
    runtime = models.IntegerField(max_length = 15, blank = True, null = True)  
    objects = ScoreManager()
    
# EOF