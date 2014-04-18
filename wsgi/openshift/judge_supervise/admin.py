from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from django.conf.urls import url, patterns

from contest.models import Contest, Team
from execution.models import Problem
from teamsubmission.models import Submission


from collections import defaultdict
from decimal import Decimal
from random import randint

ORACLE_FEEDBACK = [
        (1, 'FEED_1'),
        (2, 'FEED_2'),
        (3, 'FEED_3'),
        (4, 'FEED_4'),
        ]

class Oracle(object):
    def __init__(self, submission):
        self.text1 = ORACLE_FEEDBACK[randint(0, len(ORACLE_FEEDBACK) - 1)][1]
        self.text2 = ORACLE_FEEDBACK[randint(0, len(ORACLE_FEEDBACK) - 1)][1]
        self.text3 = ORACLE_FEEDBACK[randint(0, len(ORACLE_FEEDBACK) - 1)][1]

        self.problem= submission.problem
        self.date_uploaded = submission.date_uploaded


class FeedbackPerProblem(object):
    def __init__(self, feedback_type, problem, count):
        self.feedback_type = feedback_type
        self.problem =problem
        self.count =count

class CountFeedbackRow(object):
    def __init__(self, feedback, total, prob_count_list):
        self.feedback = feedback
        self.total = total
        self.prob_count_list = prob_count_list



class SubTeamFailedView(object):
    def __init__(self, team, problem, fail_count, prev_solved,
                 site_location = ''):
        self.team = team
        self.problem = problem
        self.fail_count = fail_count
        self.prev_solved = prev_solved
        self.site_location = site_location

class ProblemAttempsCount(object):
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

       #TODO: check out django admin tables sorters..



def get_prob_team(team):
    contest = Contest.objects.get()
    problems = Problem.objects.filter(contest=contest)


    submissions = Submission.objects.filter(team=team).order_by('-date_uploaded').order_by('problem')

    return

def get_rand_feedback():
    import random
    small_lett = [ chr(x) for x in range(97,123)]
    def id_generator(size=6, chars=small_lett):
        return ''.join(random.choice(chars) for _ in range(size))
    return id_generator()

def get_unsolved_attemps(team_list):
    onsite_list, offsite_list = [], []
    for team in team_list:
        submissions = Submission.objects.filter(team=team) \
                      .order_by('-date_uploaded').order_by('problem')

        groups = defaultdict( list )
        solved_count = 0
        for sub in submissions:
            groups[sub.problem].append(sub)
            if sub.solved_problem == True:
                solved_count += 1

        for prob in groups:
            sub_list = groups[prob]

            if any(sub.solved_problem == True for sub in sub_list):
                print "lolol"
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
    ret_list = [ ];

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

def show_view(request, team_pk, problem_pk):
    submissions = Submission.objects.filter(team=team_pk) \
                    .order_by('-date_uploaded').filter(problem=problem_pk)
    oracle_list = []

    for sub in submissions:
        oracle_list.append( Oracle(sub) )

    context = {
            'oracle_list' : oracle_list,
            }

    return render(request,
                  'judge_team_submissions.html',
                  context)

def show_prob_subs(request, problem_pk):
    context = {}

    return render(request,
                  'judge_problem_sub.html',
                  context)


def show_team(request, team_pk):
    dic = dict()
    submissions = Submission.objects.filter(team=team_pk)\
                  .order_by('-date_uploaded')
    prob_row, oracle_list = [], []
    prob_index = {}
    problems = Problem.objects.get_queryset()

    for index, val in enumerate(problems):
        prob_index[val] = index

    for sub in submissions:
        feedback = ORACLE_FEEDBACK[randint(0, len(ORACLE_FEEDBACK) - 1)][1]
        dic.setdefault(feedback, [0] * len(problems))
        #import ipdb; ipdb.set_trace()
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
            }

    return render(request,
                  'judge_team_sublist.html',
                  context)


class MyModelAdmin(admin.ModelAdmin):
    view_on_site = True
    class Media:
        pass
        """ https://docs.djangoproject.com/en/1.6/ref/contrib/admin/#django.contrib.admin.ModelAdmin.get_urls
        """
    def get_urls(self):
        urls = super(MyModelAdmin, self).get_urls()
        my_urls = patterns('',
           url(r'^my_view/$', admin.site.admin_view(self.my_view, cacheable=True)),
           url(r'^my_view/team(?P<team_pk>[0-9]+)' +
                  '/problem(?P<problem_pk>[0-9]+)/$',
                  admin.site.admin_view(show_view)),
           url(r'^my_view/problem(?P<problem_pk>[0-9]+)/$',
                  admin.site.admin_view(show_prob_subs)),
           url(r'^my_view/team(?P<team_pk>[0-9]+)',
                admin.site.admin_view(show_team)),
        )
        return my_urls + urls

    def my_view(self, request):
        contest = Contest.objects.get()
        try:
            team_list = Team.objects.filter(contest=contest)
        except ObjectDoesNotExist:
            team_list = []

        fail_count_onsite, fail_count_offsite = get_unsolved_attemps(team_list)
        prob_attempt_counts = get_attempt_count(contest)

        context = {
                'team_list' : team_list,
                'team_sub'  : get_prob_team(team_list),
                'fail_count_onsite':  fail_count_onsite,
                'fail_count_offsite':  fail_count_offsite,
                'prob_attempt_counts' : prob_attempt_counts,
                }

        return render(request,
                      'judgefeedback.html',
                      context,
                      )


from django.db import models
class DummyModel(models.Model):
    class Meta:
        managed = False
admin.site.register(DummyModel, MyModelAdmin)

# EOF
