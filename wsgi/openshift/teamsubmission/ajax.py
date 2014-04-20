'''
Created on Apr 9, 2014

@author: filip
'''
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.core.exceptions import ObjectDoesNotExist
from .models import Submission
from openshift.contest.models import Team
from openshift.contest.models import Contest
import datetime
from django.core import serializers
import json

@dajaxice_register
def ajaxalert(request):
    user = request.user
    dajax = Dajax()
    dajax.alert('Test')
    dajax.alert(user.get_full_name())
    return dajax.json()


@dajaxice_register
def submission(request, submission_id):
    dajax = Dajax()
    
    try:
        sub  = Submission.objects.get(id = int(submission_id))
    except ObjectDoesNotExist:
        sub = None
    # TODO: Filter only latest?
    members = sub.team.members.all()
    if request.user in members:
        if sub.status != Submission.EVALUATED:
            dajax.assign('#response', 'innerHTML', Submission.STATES[sub.status][1])
        else:
            dajax.script('location.reload();')
    return dajax.json()


@dajaxice_register
def get_highscore(request, contest):
    '''
    Note: contest is url!
    '''
    dajax = Dajax()
    
    #Gets the current contest
    contest = get_current_contest(contest)
    statistics = Submission.objects.get_highscore(contest)[:5]
    
    
    print statistics
    #pdb.set_trace()    
    '''
    Sort based on score, get top 5
    '''

    dajax.assign('#highscoretable', 'innerHTML', build_html_table(statistics))
    return dajax.json()

#gets the curent contest based on url string
def build_html_table(stats):
    string = ""
    for s in range(len(stats)):
        string += "<tr>"
        
        #PLACE
        string +=  "<td>" + unicode(stats[s][0]) + "</td>"
        
        #TEAM NAME
        if len(stats[s][1].encode('utf-8')) > 10:
            string += "<td>" + unicode(stats[s][1].encode("utf-8")[:10], "utf-8", errors="ignore") + "..." + "</td>"
        
	else:
            string += "<td>" + unicode(stats[s][1]) + "</td>"
        
        #Number of solved
        string += "<td>" + unicode(stats[s][2]) + "</td>"
        
        #Onsite/ofsite
        if stats[s][5] == True:
            #string += "<td>" + "<span class=\"label label-success\"> \" \" </span>"  + "</td>"
            string += "<td>" + "Yes" + "</td>"
        else: 
            string += "<td>" + "No"  + "</td>"
        
        #string += "<td>" + str(stats[s][5]) + "</td>"
        
        
        
        
        #Score
        #string += "<td>" + str(stats[s][3]) + "</td>"
        
        string += "</tr>"
    
    return string
    
def get_current_contest(url):
    try: 
        current_contest = Contest.objects.get(url = url)
    except ObjectDoesNotExist as e:
        return None
    return current_contest;

