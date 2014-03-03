#coding:utf-8
from django.shortcuts import render
from contest.forms import Team_Form 
from django.http import HttpResponseRedirect
from article.models import Article

# Create your views here.

def index(request):
    url = request.path.split('/')[1]
    article_list = Article.objects.all().filter(contest__url = url).order_by("-created_at")
    context = {'article_list' : article_list, 
               }    
    return render(request, 'contest/index.html', context)

def registration(request):
    if request.method == 'POST': # If the form has been submitted...
        # teamform is defined in openshif.contest.models
        form = Team_Form(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            '''
            TODO: prosess the data in form.cleaned_data
            '''            
            form.save() # Save the TeamForm in the database
            return HttpResponseRedirect('registrationComplete/') # Redirect after POST
    else:
        form = Team_Form() # a new form
        
    return render(request, 'registerForContest/registration.html', {
        'form': form,
    })


def registrationComplete(request):
    return render(request, 'registerForContest/registrationComplete.html')
