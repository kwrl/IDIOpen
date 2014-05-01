from django.shortcuts import render
from openshift.contest.models import Contest

def home(request):
    
    contests = Contest.objects.all()
    
    context = {'contests':contests,
               }
    
    return render(request, 'home/home.html', context)

    
