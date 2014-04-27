from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
import os
from datetime import datetime
from openshift.execution.models import Problem
from openshift.contest.models import Team
from openshift.helpFunctions.views import get_score, in_contest

from collections import defaultdict

private_media = FileSystemStorage(location=settings.PRIVATE_MEDIA_ROOT,
                                  base_url=settings.PRIVATE_MEDIA_URL,
                                  )
class TriesTimeSolved(object):
    def __init__(self, tries, attempts, solved):
        self.tries = tries
        self.attempts = attempts
        self.solved = solved

class TeamTrRow(object):
    def __init__(self, team, problemsLen):
        self.problemList = [None] * problemsLen
        self.team = team
        self.site = team.offsite
        self.total_score = 0
        self.total_time = 0
        self.total_solved = 0
        self.skill_level = '1'
        x = team.members.first()
        if x:
            self.skill_level = x.skill_level
        self.pro = False
        if self.skill_level == 'pro':
            self.pro = True

        if team.members.count() > 0:
            for member in team.members.all()[1:]:
                if member.skill_level > self.skill_level:
                    self.skill_level = member.skill_level
                    if member.skill_level == 'pro':
                        self.pro = True

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
    def get_highscore(self, contest, sort_res=''):
        teams = None
        if sort_res == 'onsite':
            teams = Team.objects.filter(contest=contest, onsite=True)
        elif sort_res == 'offsite':
            teams = Team.objects.filter(contest=contest, onsite=False)
        else:
            teams = Team.objects.filter(contest=contest)
            

        submissions = Submission.objects.all()
        team_problem_submissionscore = defaultdict( dict )
        #FIXME: assuming null
        team_problem_incorrect = defaultdict( lambda: defaultdict (int) )

        for sub in submissions:
            if not in_contest(sub, contest):
                continue
            if sub.solved_problem:
                team_problem_submissionscore[sub.team][sub.problem]  \
                    = sub; #sub.date_uploaded
            else:
                team_problem_incorrect[sub.team][sub.problem] += 1

        team_score_list = []
        # give score

        problem_index_dict = dict()
        problems = Problem.objects.all()

        for index, prob in enumerate(problems):
            problem_index_dict[prob] = index
        num_problems = problems.count()
            

        for team in teams:
            ttr = TeamTrRow(team, num_problems)
            if ttr.pro == False and sort_res == 'pro' \
            or ttr.pro == True  and sort_res == 'student':
                continue


            total_score = 0
            total_solved = 0
            for problem in problems:
                prob_index = problem_index_dict[problem]
                incorrect_count = 0
                score = ""
                solved = False
                time = ""
                sub = None
                if team_problem_incorrect[team]:
                    if problem in team_problem_incorrect[team]:
                        incorrect_count = team_problem_incorrect\
                                                [team][problem]
                if team_problem_submissionscore[team]:
                    if problem in team_problem_submissionscore[team]:
                        sub = team_problem_submissionscore[team][problem]
                        total_solved += 1
                        solved = True

                        #incorrect_count += 1 # incorrect_count also for success

                time, score = get_score(sub, incorrect_count, contest)
                ttr.total_time += time
                total_score += score
                ttr.problemList[prob_index] = TriesTimeSolved(incorrect_count,
                                                        time, solved)

            # end for problem`
            ttr.total_score = total_score
            ttr.total_solved = total_solved
            team_score_list.append(ttr)

        return team_score_list


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

