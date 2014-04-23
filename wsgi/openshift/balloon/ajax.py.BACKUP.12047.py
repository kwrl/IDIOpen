from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.core.exceptions import ObjectDoesNotExist
from openshift.teamsubmission.models import Submission


@dajaxice_register
def ajaxalert(request, contest, last_solved_submission):
    dajax = Dajax()
    
    if(check_new_submission(last_solved_submission)):
        dajax.assign('#new_balloons', 'innerHTML', '  Refresh - new submission ')
    else:
        dajax.assign('#new_balloons', 'innerHTML', '  Refresh')
        
    return dajax.json()

def check_new_submission(last_solved_submission):
    new_solved_submission = Submission.objects.filter(team__onsite = 'True').filter(solved_problem = 'True')
    new_solved_submission = new_solved_submission.latest('date_uploaded')
        
    if not (last_solved_submission == str(new_solved_submission.pk)):
        #refresh the page
        return True
    else: 
        #do nothing
        return False
    


<<<<<<< HEAD
=======

>>>>>>> 89bf6c75c3d4d9fa45347ab5d9d434c979881da1
