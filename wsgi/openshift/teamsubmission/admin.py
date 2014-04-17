from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from contest.models import Contest, Team
from execution.models import Problem
from .models import Submission

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

def get_prob_team(team):
    contest = Contest.objects.get()
    problems = Problem.objects.filter(contest=contest)


    submissions = Submission.objects.filter(team=team).order_by('-date_uploaded').order_by('problem')

    return 
    
from django.conf.urls import patterns
from django.http import HttpResponse

def get_rand_feedback():
    import random
    small_lett = [ chr(x) for x in range(97,123)]
    def id_generator(size=6, chars=small_lett):
        return ''.join(random.choice(chars) for _ in range(size))
    return id_generator()

def my_view(request):
    # TODO: get conte
    context = {}
    contest = Contest.objects.get()
    try:
        team_list = Team.objects.filter(contest=contest)
    except ObjectDoesNotExist:
        messages.info(request, "Something went wrong :(")

    import ipdb; ipdb.set_trace()
    for team in team_list:
        submissions = Submission.objects.filter(team=team).order_by('-date_uploaded').order_by('problem')
        # submission has solved.. so sort


    problems = Problem.objects.filter(contest=con).order_by('title')
    

    new_dict = dict()
    listProbSub = []
    
    for sub in submissions:
        new_dict[sub.problem] = sub
    for prob in problems:
        if prob in new_dict:
            sub = new_dict[prob]
        else:
            sub = None
        listProbSub.append((SubJoinProb(sub, prob, 
                Submission.objects.get_problem_score(team, prob, con)))
        )
    

    context = {
            'team_list' : team_list,
            'prob_sub'  : get_prob_team(team_list),
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
