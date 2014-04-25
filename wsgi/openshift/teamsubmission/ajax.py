'''
Created on Apr 9, 2014

@author: filip, typo
'''

from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.core.exceptions import ObjectDoesNotExist
from .models import Submission
import operator
from .models import TeamTrRow
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

"""
class TeamTrRow():
    def __init__(self, team, problemsLen):
        self.problemList = [None] * problemsLen
        self.team = team
        self.site = team.offsite
        self.total_score = 0
        self.total_time = 0
        self.total_solved = 0
        
         [position, - 0
        team name, - 1
        offsite, - 2
        solved problems, - 3
        total score, - 4
        total time (in minutes), - 5
        year, - 6
        gender, - 7
        problem 1 submissions, - 8
"""
@dajaxice_register
def get_highscore(request, contest):
    #contest is first URL
    dajax = Dajax()
    
    #Gets the current contest
    contest = get_current_contest(contest)
    if not show_contest(contest):
        dajax.assign('#highscore_done', 'innerHTML', build_closed_string(contest))
        return dajax.json()
    
    stats = Submission.objects.get_highscore(contest)[:5]
    
    test = build_html_table(stats.)
    import ipdb; ipdb.set_trace()
    
    dajax.assign('#highscoretable', 'innerHTML', build_html_table(stats))
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
    stats.sort(key=operator.attrgetter('total_score'), reverse=False)
    
    string = ""
    for s in range(len(stats)):
        string += "<tr>"
        
        #PLACE
        string +=  "<td>" + unicode(s) + "</td>"
        
        #TEAM NAME
        teamname = stats[s].team.name.encode('utf-8')
        if len(teamname) > 10:
            string += "<td>" + unicode(stats[s][1].encode("utf-8")[:10], "utf-8", errors="ignore") + "..." + "</td>"
        else:
            string += "<td>" + unicode(stats[s][1]) + "</td>"
        
        #Number of solved
        string += "<td>" + unicode(stats[s][3]) + "</td>"
        
        #Onsite/ofsite
        if stats[s][2]:
            #string += "<td>" + "<span class=\"label label-success\"> \" \" </span>"  + "</td>"
            if len(unicode(stats[s][2])) > 4:
                string += "<td>" + unicode(stats[s][2])[:4] + ".." "</td>"
            else:
                string += "<td>" + stats[s][2] + "</td>"
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

