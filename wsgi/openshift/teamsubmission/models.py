from django.db import models

from django.conf import settings

import os
from datetime import datetime
from openshift.execution.models import Problem
from openshift.contest.models import Team
from django.core.files.storage import FileSystemStorage

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
        [total score,                - 0
        time submitted (in minutes), - 1
        submission score,            - 2
        number of submissions]       - 3
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
    
    def get_team_score(self, team, contest, problems):
        
        """ 
        The statistics are:
        [offsite,                            - 0
        solved problems,                     - 1
        total score,                         - 2
        time submitted (in minutes),         - 3
        year,                                - 4
        gender,                              - 5
        problem 1 submissions/time solved,   - 6
        ...                                  - .
        problem n submissions/time solved]   - n
        """
         
        statistics = [0, 0, 0, 0, 0, 0]
        statistics[0] = team.offsite
        statistics[4] = team.members.all()[0].skill_level
        statistics[5] = team.members.all()[0].gender
        for member in team.members.all():
            if member.skill_level != statistics[4]:
                statistics[4] = "-"
            if member.gender != statistics[5]:
                statistics[5] = "-"
                
        for problem in problems:
            problemStat = ScoreManager.get_problem_score(self, team, problem, contest)
            if problemStat[0]:
                statistics[1] = statistics[1] + 1
            statistics[2] = statistics[2] + problemStat[0]
            statistics[3] = statistics[3] + problemStat[1]
            if(problemStat[1]):
                statistics.append(str(problemStat[3]) + "/" + str(problemStat[1]))
            else:
                statistics.append(str(problemStat[3]) + "/-")
        return statistics
    
    def get_highscore(self, contest):
        teams = Team.objects.filter(contest=contest)
        problems = Problem.objects.filter(contest=contest)
        
        """ 
        The statistics are a list of teams with:
        [position,                - 0
        team name,                - 1
        offsite,                  - 2
        solved problems,          - 3
        total score,              - 4
        total time (in minutes),  - 5
        year,                     - 6
        gender,                   - 7
        problem 1 submissions,    - 8
        ...                       - .
        problem n submissions,]   - n
        """
        statistics = []
        
        """ 
        zeros is a list of teams that have 0 in total score. These teams haven't
        solved any problems, and should be at the bottom of the scoreboard.
        """
        zeros = []
        for team in teams:
            teamStats = ScoreManager.get_team_score(self, team, contest, problems)
            highscore = [0, team.name]
            if(teamStats[1]):
                for field in teamStats:
                    highscore.append(field)
                statistics.append(highscore)
            else:
                teamStats[1] = ""
                for field in teamStats:
                    highscore.append(field)
                zeros.append(highscore)
        statistics = sorted(statistics, key=lambda x : (-x[3], x[4]))
        for i in range(len(statistics)):
            statistics[i][0] = i + 1
        
        lowestPlace = len(statistics)
        for s in zeros:
            s[0] = lowestPlace + 1
            statistics.append(s)
        return statistics
    

def file_function(instance, filename):
    return '/'.join(['submissions', str(instance.team.contest.id), str(instance.team.id), 
				    str(instance.problem.id), datetime.strftime(datetime.now(), '%d%m%y%H%M%S'), filename])


class Submission(models.Model):
    
    NOTSET = 0
    QUEUED = 1
    RUNNING = 2
    EVALUATED = 3
    STATES = (
        (NOTSET, 'Not Set'),
        (QUEUED, 'Queued'),
        (RUNNING, 'Running'),
        (EVALUATED, 'Evaluated'),
    )
    #We should rename submission field.... 
    submission = models.FileField(storage=private_media, upload_to=file_function)
    status = models.IntegerField(choices=STATES, default=NOTSET)
    compileProfile = models.ForeignKey('execution.CompilerProfile')
    date_uploaded = models.DateTimeField(auto_now = True)
    solved_problem = models.BooleanField(default=False) #E.g. Did this submission solve the the problem
    text_feedback = models.CharField(max_length=50)
    team = models.ForeignKey('contest.Team')
    problem = models.ForeignKey('execution.Problem')
    runtime = models.IntegerField(max_length = 15, blank = True, null = True)  
    objects = ScoreManager()

    def __unicode__(self):
        return unicode(self.pk)

class ExecutionLogEntry(models.Model):
    submission  = models.ForeignKey(Submission)
    command     = models.CharField(help_text="Command issued", max_length=200)
    stdout      = models.TextField(help_text="Standard output")
    stderr      = models.TextField(help_text="Standard error")
    retval      = models.IntegerField(help_text="Return value")

    def __unicode__(self):
        return "Submission:\t" + unicode(self.submission.pk) + "\tCommand:\t " + self.command
    
# EOF
