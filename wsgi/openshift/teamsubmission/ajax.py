'''
Created on Apr 9, 2014

@author: filip
'''
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
import datetime

@dajaxice_register
def ajaxalert(request):
    user = request.user
    dajax = Dajax()
    dajax.alert('Test')
    dajax.alert(user.get_full_name())
    return dajax.json()


@dajaxice_register
def submission(request):
    dajax = Dajax()
    now = str(datetime.datetime.now())
    dajax.assign('#response', 'innerHTML', now)
    return dajax.json()
