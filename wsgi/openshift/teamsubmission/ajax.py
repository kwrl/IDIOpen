'''
Created on Apr 9, 2014

@author: filip, typo
'''

from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.core.exceptions import ObjectDoesNotExist
from .models import Submission
from openshift.contest.models import Contest
import datetime
from datetime import timedelta
from django.utils.timezone import utc
CLOSE_TIME = 1 #Hour

@dajaxice_register
def ajaxalert(request):
    user = request.user
    dajax = Dajax()
    dajax.alert('Test')
   #s dajax.alert(user.get_full_name())
    return dajax.json()


@dajaxice_register
def submission(request, submission_id):
    dajax = Dajax()    
    try:
        sub  = Submission.objects.get(id = int(submission_id))
    except ObjectDoesNotExist:
        sub = None
        return dajax.json()
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
    #contest is first URL
    dajax = Dajax()
    
    #Gets the current contest
    contest = get_current_contest(contest)
    if not show_contest(contest):
        dajax.assign('#highscore_done', 'innerHTML', build_closed_string(contest))
        return dajax.json()
    
    statistics = Submission.objects.get_highscore(contest)[:5]
    dajax.assign('#highscoretable', 'innerHTML', build_html_table(statistics))
    return dajax.json()


'''
Returns false if highscore should be hidden
'''
def show_contest(contest):
    
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    day = datetime.date.today()
    
    #We subtract on hour    
    close_time_first = contest.end_date-timedelta(hours=CLOSE_TIME)
    close_time_completed = contest.end_date
    
    if (now > close_time_first and now < close_time_completed):
        return False
    else:
        return True

    
    
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
        string += "<td>" + unicode(stats[s][3]) + "</td>"
        
        #Onsite/ofsite
        if stats[s][5]:
            #string += "<td>" + "<span class=\"label label-success\"> \" \" </span>"  + "</td>"
            if len(stats[s][2]) > 3: 
                string += "<td>" + stats[s][2][:3] + ".." "</td>"
            else:
                string += "<td>" + stats[s][2][:3] + "</td>"
        else: 
            string += "<td>" + "Yes"  + "</td>"
        
        #string += "<td>" + str(stats[s][5]) + "</td>"
        #Score
        
        #string += "<td>" + str(stats[s][3]) + "</td>"
        string += "</tr>"
    
    return string


def build_closed_string(contest):
    close_time_first = contest.end_date-timedelta(hours=CLOSE_TIME)
    close_time_completed = contest.end_date
    return "<smalL> Highscore frozen.  </small>"
    #delta = close_time_completed - close_time_first
    
    
def get_current_contest(url):
    try: 
        current_contest = Contest.objects.get(url = url)
    except ObjectDoesNotExist as e:
        return None
    return current_contest;

