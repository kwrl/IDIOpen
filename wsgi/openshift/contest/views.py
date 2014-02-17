from django.shortcuts import render
from openshift.contest.models import Contest
# Create your views here.

def index(request, url):
    contest = Contest.objects.get(url=url)
    context = {'contest': contest}
    return render(request, 'home/home.html', context)