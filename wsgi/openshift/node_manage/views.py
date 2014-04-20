from django.shortcuts import render, HttpResponse

# Create your views here.

from openshift.node_manage.tasks import evaluate_task

def index(request):
    #res = add.delay(1, 1)
    #res = evaluate_task(1,1,[1],1)
    #res = uname()
    return HttpResponse('The lamest easter egg ever.')
