#coding:utf-8
from django.shortcuts import render
from contest.forms import Team_Form 
from django.http import HttpResponseRedirect
from article.models import Article
from userregistration.models import CustomUser
from userregistration.models import CustomUserManager


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
            new_team = form.save(commit=False)
            email_one = form.cleaned_data['email_one']
            email_two = form.cleaned_data['email_two']  
            '''
            TODO: prosess the data in form.cleaned_data
            ''' 
            if not(user_exist(email_one)): # returns True if the user e
                new_user = CustomUser.objects.create_user(email_one, "<insertName>", "<insertName>", "eple1")                
                new_user = CustomUser.objects.create_inactive_user(email_one, "PenisFjes", "Håkon", "tiss", "google.no", "google.no", True)
        
                new_user.save()
                
            form.save() # Save the TeamForm in the database
            return HttpResponseRedirect('registrationComplete/') # Redirect after POST
    else:
        form = Team_Form() # a new form
        
    return render(request, 'registerForContest/registration.html', {
        'form': form,
    })


def registrationComplete(request):
    return render(request, 'registerForContest/registrationComplete.html')

'''
This function checks if the user exist (is in the database)
'''

def user_exist(email):
    if CustomUser.objects.filter(email = email):
        return True
    return False
    
