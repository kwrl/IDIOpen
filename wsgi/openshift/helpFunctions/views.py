#coding:utf-8
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from openshift.contest.models import Contest
from openshift.contest.models import Team
from openshift.clarification.models import QuestionAnswer
from django.shortcuts import get_object_or_404


import datetime;
from django.utils import timezone;

def in_contest(submission, contest):
#The alternative, giving each balloon a contest key, is feasible.
#    However, the chain goes on: why not give a submissions a relation?
#
#    Instead of thinking and performing a large refactoring, I wrote this...
    # After all, it's "only" 2 chains...
    return contest.pk == submission.team.contest.pk



def get_score(sub, incorrect_count, contest):
    if not sub:
        return 0, 0

    time = int((sub.date_uploaded
            - contest.start_date).total_seconds()) / 60
    # FIXME: floating point?
    return time, time + (incorrect_count * contest.penalty_constant) 


'''
This view is supposed to hold functions used by several modules. 
Please mark 
'''

def date_in_range(dateobject, start, end):
    return (start <= dateobject and dateobject  <= end)

def plausible_today_contest():
    today = getTodayDate()
    contests = Contest.objects.all()

    return next((con for con in contests \
            if date_in_range(today, con.start_date, con.end_date)), None)

def get_most_plausible_contest(contest_pk=None):
    given_contest = None
    if contest_pk:
        try:
            given_contest = Contest.objects.get(id=contest_pk)
        except TypeError:
            pass

    return next((x for x in [given_contest, plausible_today_contest(), \
                    Contest.objects.earliest('teamreg_end_date')] \
                        if x is not None),
                None)

# Returns the current contest.
def get_current_contest(request):
    try: 
        current_contest = Contest.objects.get(url = get_current_url(request))
    except ObjectDoesNotExist as e:
        raise Http404
    return current_contest;

#Return the date of today
def getTodayDate():
    return timezone.make_aware(datetime.datetime.now(),
                               timezone.get_default_timezone());
                               
    
# Returns the current url
def get_current_url(request):
    try: 
        url = request.path.split('/')[1]
    except ObjectDoesNotExist as e: 
        raise Http404
    return url; 


def get_team(request):
    '''
    This function returns the current team. 
    The current team is the team that corresponds to the current contest, and user. 
    '''
    user = request.user
    con = get_current_contest(request)
    queryset = Team.objects.filter(contest=con).filter(members__in = [user])
    team = get_object_or_404(queryset)
    return team

def contest_begin(request):
    try: 
        contest = get_current_contest(request)
        startDate = contest.start_date
        dateToday = timezone.now()
        if (dateToday >= startDate):
            has_started = True
        else:
            has_started = False
    except ObjectDoesNotExist as e: 
        raise Http404
    return has_started

#===============================================================================
# Check if user is on a team
#===============================================================================
def is_member_of_team(request):
    contest = get_current_contest(request)
    team = Team.objects.filter(contest=contest).filter(members__id = request.user.id)
    if team.count() > 0:
        return team[0]
    else:
        team = False


#===============================================================================
# Returns all the ansswers for a contest based on a request. 
#===============================================================================
def get_all_answers(request):
    contest = get_current_contest(request)
    answers = QuestionAnswer.objects.filter(contest=contest).order_by("-answered_at")
     
    if(answers.count() < 0):
        return None
    return answers
      
    

