#coding:utf-8
from django.shortcuts import render
from contest.forms import Team_Form 
from django.http import HttpResponseRedirect
from article.models import Article
from userregistration.models import CustomUser
from userregistration.models import CustomUserManager
from contest.models import Team, Invite
from django.contrib.auth import get_user_model
from django.contrib.sites.models import get_current_site
from django.contrib.auth.decorators import login_required


User = get_user_model()
# Create your views here.

def index(request):
    url = request.path.split('/')[1]
    article_list = Article.objects.all().filter(contest__url = url).order_by("-created_at")
    context = {'article_list' : article_list, 
               }    
    return render(request, 'contest/index.html', context)

# @login_required
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
            team = Team.objects.create(team_name=form.cleaned_data['team_name'], onsite=form.cleaned_data['onsite'], 
                                       offsite=form.cleaned_data['offsite'])            
            '''
            TODO:  This should be a loop, looping over the number allowed members. But first  
            '''
            site = get_current_site(request)
            url = request.path.split('/')[1]
            
            
            invite_1 =Invite.objects.create_invite(email = email_one, team=team, url=url, site=site); # adding "user" (a.k.a the email) to invite list.
            invite_1.save()  
            invite_2 = Invite.objects.create_invite(email = email_two, team=team, url=url, site=site); # adding "user" (a.k.a the email) to invite list. 
            invite_2.save()
            '''
            Checking wether or not a user with that email exist is done in userregistration.
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

'''
This function checks if the user exist (is in the database)
'''

def user_exist(email):
    if CustomUser.objects.filter(email = email):
        return True
    return False
    
