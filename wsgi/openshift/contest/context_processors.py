'''
Created on Feb 19, 2014

@author: filip
'''
from django.core.exceptions import ObjectDoesNotExist
from contest.models import Contest

'''
Currently not used
'''
def contest(request):
    """
    return the current contest
    """
    url = request.path.split('/')[1]
    try:
        contest = Contest.objects.get(url=url)
    except ObjectDoesNotExist:
        contest = None
        #raise Http404
    return {'contest': contest}