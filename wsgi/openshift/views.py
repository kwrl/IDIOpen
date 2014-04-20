from django.shortcuts import render
from openshift.contest.models import Contest
from openshift.contest.tasks import add, xsum

def home(request):
    
    contests = Contest.objects.all()
    
    context = {'contests':contests,
               }
    
    return render(request, 'home/home.html', context)

def taskTest(request):
    
    result = add.delay(3,2)
    print result.ready()
    numbers = [1,2,3,4,5]
    
    res = xsum(numbers)
    print result
    print res
    
    contests = Contest.objects.all()
    context = {'contests':contests,
               }
    
    return render(request, 'home/home.html', context)
    
