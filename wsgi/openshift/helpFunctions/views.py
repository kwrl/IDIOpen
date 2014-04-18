#coding:utf-8
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from contest.models import Contest
from contest.models import Team
from django.shortcuts import get_object_or_404


import datetime;
from django.utils import timezone;

'''
This view is suppose to hold functiones used by several modules. 
Please mark 
'''

# Returns the current contest.
def get_current_contest(request):
    try: 
        current_contest = Contest.objects.get(url = get_current_url(request))
    except ObjectDoesNotExist as e:
        raise Http404
    return current_contest;

#Return the date of today
def getTodayDate(request):
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