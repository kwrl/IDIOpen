from django.shortcuts import render, HttpResponse

# Create your views here.

from openshift.node_manage.tasks import add, evaluate_task, uname

def index(request):
    #res = add.delay(1, 1)
    res = evaluate_task(0,0,[0],0)
    #res = uname()
    return HttpResponse('<p>' + str(res)  + '</p>')
