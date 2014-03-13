#coding:utf-8
from django.shortcuts import render
from contest.forms import Team_Form 
from django.http import HttpResponseRedirect
from article.models import Article
from userregistration.models import CustomUser
from userregistration.models import CustomUserManager
from contest.models import Team, Invite, Contest
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
    messages = []
    if request.method == 'POST': # If the form has been submitted...
        # teamform is defined in openshif.contest.models
        form = Team_Form(request.POST) # A form bound to the POST data
         
        if form.is_valid(): # All validation rules pass
            #new_team = form.save(commit=False)
            email_one = form.cleaned_data['email_one']
            email_two = form.cleaned_data['email_two'] 
            
            '''
            We need to check if the emails are equal. You should not be able to use to equal emails.
            '''
            if (email_one == email_two):
                messages.append({'text':'Please do not use equal emails','error':'alert-danger'})                
                            
                
            else: # if the emails do not equal each other
                
                '''
                TODO: add this in try/catch
                '''
                url = request.path.split('/')[1]
                current_contest = Contest.objects.get(url = url)
                
                team = Team.objects.create(name=form.cleaned_data['name'], onsite=form.cleaned_data['onsite'], 
                                           offsite=form.cleaned_data['offsite'], contest = current_contest)
                                            
                
                '''
                TODO:  This should be a loop, looping over the number allowed members. For now this will be OK.  
                '''
                site = get_current_site(request)
                
                if email_one:
                    invite_1 =Invite.objects.create_invite(email = email_one, team=team, url=url, site=site); # adding "user" (a.k.a the email) to invite list.
                    invite_1.save()
                
                if email_two:
                    invite_2 = Invite.objects.create_invite(email = email_two, team=team, url=url, site=site); # adding "user" (a.k.a the email) to invite list. 
                    invite_2.save()
                    
                '''
                Checking if a user with that email exist is done in userregistration.
                '''                         
                #form.save() # Save the TeamForm in the database
                return HttpResponseRedirect('registrationComplete/') # Redirect after POST, sends you to complete
                #end else
            return render(request, 'registerForContest/registration.html', {
                    'form': form,
                    'messages':messages,
                    })
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

'''
AUTHOR: Haakon
but.. it is not working...
'''
@login_required
def teamProfil(request):    
    user = request.user
    url = request.path.split('/')[1]
    
    team = Team.objects.filter(members__id = user.id)[0]
    context = {'team':team}
    return render(request, 'contest/team.html', context)

