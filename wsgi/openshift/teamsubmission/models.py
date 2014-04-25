from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
import os
from datetime import datetime
from openshift.execution.models import Problem
from openshift.contest.models import Team

from collections import defaultdict

private_media = FileSystemStorage(location=settings.PRIVATE_MEDIA_ROOT,
                                  base_url=settings.PRIVATE_MEDIA_URL,
                                  )
class TeamTrRow():
    def __init__(self, team):
        self.team = team
        self.onsite = team.onsite
        self.total_score = 0
        self.num_solved = 0

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
    def get_problem_score(self, problem, contest, submissions):

        """
        This constant is the penalty
        for delivering incorrect submissions.
        """
        submission_penalty = contest.penalty_constant
        incorrectSubmissions = []
        correctSubmissions = []
        for submission in submissions:
            if(submission.solved_problem):
                correctSubmissions.append(submission)
            else:
                incorrectSubmissions.append(submission)

        """
        The statistics are:
        [total score,                - 0
        time submitted (in minutes), - 1
        submission score,            - 2
        number of submissions]       - 3
        """
        statistics = [0, 0, 0, len(incorrectSubmissions)]
        if correctSubmissions:
            time = int((correctSubmissions[0].date_uploaded - problem.contest.start_date).total_seconds()) / 60
            submissionScore = len(incorrectSubmissions) * submission_penalty

            statistics[0] = time + submissionScore
            statistics[1] = time
            statistics[2] = submissionScore
            statistics[3] = len(incorrectSubmissions) + 1
        return statistics

    def get_team_score(self, team, contest, problems, submissions):

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
        if team.members.all():
            statistics[4] = team.members.all()[0].skill_level
            statistics[5] = team.members.all()[0].gender
        for member in team.members.all():
            if member.skill_level != statistics[4]:
                statistics[4] = "-"
            if member.gender != statistics[5]:
                statistics[5] = "-"

        for problem in problems:
            problemSubmissions = []
            for submission in submissions:
                if(submission.problem == problem):
                    problemSubmissions.append(submission)
            problemStat = ScoreManager.get_problem_score(self, problem, contest, problemSubmissions)
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
        teams = Team.objects.all()
        submissions = Submission.objects.all()
        team_problem_submissionscore = defaultdict( dict )
        #FIXME: assuming null
        team_problem_incorrect = defaultdict( defaultdict (int) )

        for sub in submissions:
            if sub.is_valid:
                team_problem_submissionscore[sub.team][sub.problem]  \
                    = sub.date_uploaded
            else:
                team_problem_incorrect[sub.team][sub.problem] += 1

        team_score_list = []
        # give score

        for team in teams:
            ttr = TeamTrRow(team)
            total_score = 0
            num_solved = 0
            for problem in team_problem_submissionscore[team]:
                if team_problem_submissionscore[team][problem]:
                    sub = team_problem_submissionscore[team][problem]
                    num_solved += 1
                    incorrect_count = 0
                    if team_problem_incorrect[sub.team][sub.problem]:
                        incorrect_count = team_problem_incorrect\
                                                [sub.team][sub.problem]
                    time, score = get_score(sub, incorrect_count, contest)
                    total_score += score
                    ttr.total_time += time
            # end for problem`
            ttr.total_score = total_score
            ttr.num_solved = num_solved
            team_score_list.append(ttr)

        return team_score_list

def get_score(sub, incorrect_count, contest):
    time = int((sub.date_uploaded
            - contest.start_date).total_seconds()) / 60
    # FIXME: floating point?
    return time, (incorrect_count * contest.submission_penalty) 





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
