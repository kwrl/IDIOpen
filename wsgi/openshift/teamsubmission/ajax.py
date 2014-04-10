'''
Created on Apr 9, 2014

@author: filip
'''
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
@dajaxice_register
def ajaxalert(request):
    dajax = Dajax()
    dajax.alert("test")
    return dajax.json()