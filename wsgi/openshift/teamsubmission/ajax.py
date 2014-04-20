'''
Created on Apr 9, 2014

@author: filip
'''
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.core.exceptions import ObjectDoesNotExist
from .models import Submission
from openshift.contest.models import Team
import datetime

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
