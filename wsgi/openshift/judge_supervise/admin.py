from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.conf.urls import url, patterns

from openshift.contest.models import Contest, Team
from openshift.execution.models import Problem
from openshift.teamsubmission.models import Submission

from collections import defaultdict
from decimal import Decimal

ORACLE_FEEDBACK = [
        (1, 'FEED_1'),
        (2, 'FEED_2'),
        (3, 'FEED_3'),
        (4, 'FEED_4'),
        ]

class Oracle(object):
    """ Return some random feedback"""
    def __init__(self, submission):
        from random import randint
        self.text1 = ORACLE_FEEDBACK[randint(0, len(ORACLE_FEEDBACK) - 1)][1]
        self.text2 = ORACLE_FEEDBACK[randint(0, len(ORACLE_FEEDBACK) - 1)][1]
        self.text3 = ORACLE_FEEDBACK[randint(0, len(ORACLE_FEEDBACK) - 1)][1]

        self.problem= submission.problem
        self.date_uploaded = submission.date_uploaded


class FeedbackPerProblem(object):
    """ Collection of data
    """
    def __init__(self, feedback_type, problem, count):
        self.feedback_type = feedback_type
        self.problem =problem
        self.count =count

class CountFeedbackRow(object):
    """ Collection of data
    """
    def __init__(self, feedback, total, prob_count_list):
        self.feedback = feedback
        self.total = total
        self.prob_count_list = prob_count_list



class SubTeamFailedView(object):
    """ Collection of data
    """
    def __init__(self, team, problem, fail_count, prev_solved,
                 site_location = ''):
        self.team = team
        self.problem = problem
        self.fail_count = fail_count
        self.prev_solved = prev_solved
        self.site_location = site_location

class ProblemAttempsCount(object):
    """ Collection of data
    """
    def __get_ratio(self):
        if self.successfull == 0:
            return 0
        if self.failed == 0:
            return self.successfull

        return Decimal(self.successfull / self.failed)

    def __init__(self, problem, failed, successfull):
        self.problem = problem
        self.failed = failed
        self.successfull = successfull
        self.total = failed + successfull
        self.success_ratio = self.__get_ratio()

class MyModelAdmin(admin.ModelAdmin):
    # FIXME
    """ Temporary solution to get a view connected in admin site
    """
    view_on_site = True
    class Media:
        """ https://docs.djangoproject.com/en/1.6/ref/contrib/
            admin/#django.contrib.admin.ModelAdmin.get_urls
        """
    def get_urls(self):
        urls = super(MyModelAdmin, self).get_urls()
        my_urls = patterns('',
           url(r'^my_view/$', admin.site.admin_view(judge_home,
                                                    cacheable=True)),
           url(r'^my_view/team(?P<team_pk>[0-9]+)' +
                  '/problem(?P<problem_pk>[0-9]+)/$',
                  admin.site.admin_view(judge_submission_team)),
           url(r'^my_view/team(?P<team_pk>[0-9]+)',
                admin.site.admin_view(judge_team_summary)),
        )

        return my_urls + urls

def get_unsolved_attemps(team_list):
    """ For all the problems, per team,
        extract tuples off teams that have tried X times to solve a problem
        without success
    """
    onsite_list, offsite_list = [], []
    for team in team_list:
        submissions = Submission.objects.filter(team=team) \
                      .order_by('-date_uploaded').order_by('problem')

        prob_to_subs_dict = defaultdict( list )
        solved_count = 0
        for sub in submissions:
            if sub.solved_problem == True:
                solved_count += 1
            prob_to_subs_dict[sub.problem].append(sub)

        for prob in prob_to_subs_dict:
            sub_list = prob_to_subs_dict[prob]

            if any(sub.solved_problem == True for sub in sub_list):
                """ Ignore the count of submissions if the team has solved
                    the problem
                """
                continue
            else:
                if team.onsite == True:
                    stfv = SubTeamFailedView(team=team, problem=prob,
                                             fail_count=len(sub_list),
                                             prev_solved=solved_count )
                    onsite_list.append(stfv)
                else:
                    stfv = SubTeamFailedView(team=team, problem=prob,
                                             fail_count=len(sub_list),
                                             prev_solved=solved_count,
                                             site_location = team.offsite)
                    offsite_list.append(stfv)

    return onsite_list, offsite_list

def get_attempt_count(contest):
    problems = Problem.objects.filter(contest=contest).order_by('title')
    submissions = Submission.objects.get_queryset()
    groups = defaultdict( list )
    ret_list = [ ]

    for sub in submissions:
        groups[sub.problem].append(sub)

    for prob in problems:
        failed_for_problem, succeded_for_problem = 0, 0
        for sub in groups[prob]:

            if sub.solved_problem:
                succeded_for_problem += 1
            else:
                failed_for_problem += 1

        ret_list.append( ProblemAttempsCount(problem=prob,
                                            failed=failed_for_problem,
                                            successfull=succeded_for_problem
                                            ))
    return ret_list

def judge_submission_team(request, team_pk, problem_pk):
    submissions = Submission.objects.filter(team=team_pk) \
                    .order_by('-date_uploaded').filter(problem=problem_pk)
    oracle_list = []

    for sub in submissions:
        oracle_list.append( Oracle(sub) )

    context = {
            'oracle_list' : oracle_list,
            'team': Team.objects.get(pk=team_pk),
            }

    return render(request,
                  'judge_team_summary.html',
                  context)

def judge_team_summary(request, team_pk):
    """ The page to render an overview of the team
    """
    dic = dict()
    submissions = Submission.objects.filter(team=team_pk)\
                  .order_by('-date_uploaded')
    prob_row, oracle_list = [], []
    prob_index = {}
    problems = Problem.objects.get_queryset() # all problems

    for index, val in enumerate(problems):
        prob_index[val] = index

    for sub in submissions:
        from random import randint
        feedback = ORACLE_FEEDBACK[randint(0, len(ORACLE_FEEDBACK) - 1)][1]
        dic.setdefault(feedback, [0] * len(problems))
        dic[feedback][prob_index[sub.problem]] += 1

        oracle_list.append( Oracle(sub) )

    total_count = dict([(key,sum(val)) for key,val in dic.iteritems()])

    for key, val in dic.iteritems():
        prob_row.append(CountFeedbackRow(feedback = key,
                                         total=total_count[key],
                                         prob_count_list = val))

    context = {
            'oracle_list' : oracle_list,
            'problems' : problems,
            'prob_row' : prob_row,
            'team': Team.objects.get(pk=team_pk),
            }

    return render(request,
                  'judge_team_summary.html',
                  context)


def judge_home(request):
    contest = Contest.objects.get()
    try:
        team_list = Team.objects.filter(contest=contest)
    except ObjectDoesNotExist:
        team_list = []

    fail_count_onsite, fail_count_offsite = get_unsolved_attemps(team_list)
    prob_attempt_counts = get_attempt_count(contest)

    context = {
            'team_list' : team_list,
            'fail_count_onsite':  fail_count_onsite,
            'fail_count_offsite':  fail_count_offsite,
            'prob_attempt_counts' : prob_attempt_counts,
            }

    return render(request,
                  'judge_home.html',
                  context,
                  )


from django.db import models
class DummyModel(models.Model):
    class Meta:
        managed = False
admin.site.register(DummyModel, MyModelAdmin)

# EOF
