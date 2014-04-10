from django.shortcuts import render, HttpResponse

# Create your views here.

from openshift.node_manage.tasks import add

def index(request):
    res = add.delay(1, 1)

    return HttpResponse('<p>' + str(res.get(1))  + '</p>')
