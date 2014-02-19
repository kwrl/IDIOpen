from django.shortcuts import render
from openshift.contest.models import Contest
# Create your views here.

def index(request):
    return render(request, 'base.html')