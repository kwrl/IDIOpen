from django.contrib import admin, messages
from django.core.exceptions import ObjectDoesNotExist
from django.conf.urls import patterns
from django.http import HttpResponse
from django.shortcuts import render

from contest.models import Contest, Team
from execution.models import Problem
from .models import Submission

from collections import defaultdict

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('date_uploaded', 'text_feedback', 'team', 'problem', 'solved_problem', 'submission')


class JudgeFeedbackAdmin(admin.ModelAdmin):
    ## get all subs from all teams
    ## sort all per team per sub

    ## this should be showable in admin

    ## clickable on problem for a team, see sections

    ### TODO: how do I get the actual info? What kind of code messages can
    # I expect?
    pass

""" get every where there is > 1 submission and problem not completed
"""
""" for each problem
        group all submissions for prob by team
        ignore where completed = true
                put on top for > 1 submission

"""
""" select team, then a list of problems come with submissions
        can sort by latest submissions
"""

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

class SubTeamFailedView(object):
    def __init__(self, team, problem, fail_count, prev_solved):
        self.team = team
        self.problem = problem
        self.fail_count = fail_count
        self.prev_solved = prev_solved

def get_unsolved_attemps(team_list):
    ret_list = []
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
                continue
            else:
                # fail_count.append(len(sub_list))
                stfv = SubTeamFailedView(team=team, problem=prob,
                                         fail_count=len(sub_list),
                                         prev_solved=solved_count )
                ret_list.append(stfv)

    return ret_list

class ProblemAttempsCount(object):
    def __init__(self, problem, failed, successfull):
        self.problem = problem 
        self.failed = failed
        self.successfull = successfull


#TODO: check out django admin tables sorters..

def get_attempt_count(contest):
    problems = Problem.objects.filter(contest=contest).order_by('title')
    submissions = Submission.objects.get_queryset()
    groups = defaultdict( list )
    ret_list = [ ];

    for sub in submissions:
            groups[sub.problem].append(sub)

    for prob in problems:
        failed_for_problem = sum([count for count in groups[prob] \
                                    if count.solved_problem])
        ret_list.append( ProblemAttempsCount(problem=prob, 
                                            failed=len(groups[prob]),
                                            ))

    return ret_list

def my_view(request):
    context = {}
    contest = Contest.objects.get()
    try:
        team_list = Team.objects.filter(contest=contest)
    except ObjectDoesNotExist:
        messages.info(request, "Something went wrong :(")

    fail_count = get_unsolved_attemps(team_list)
    #prob_attempt_counts = get_attempt_count(contest)

    context = {
            'team_list' : team_list,
            'team_sub'  : get_prob_team(team_list),
            'fail_count':  fail_count,
            #'prob_attempt_counts' : prob_attempt_counts,
            }

    return render(request,
                  'judgefeedback.html',
                  context,
                  )

def get_admin_urls(urls):
    def get_urls():
        my_urls = patterns('',
            (r'^my_view/$', admin.site.admin_view(my_view))
        )
        return my_urls + urls
    return get_urls

admin_urls = get_admin_urls(admin.site.get_urls())
admin.site.get_urls = admin_urls


admin.site.register(Submission, SubmissionAdmin)

# EOF
