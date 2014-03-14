#coding:utf-8
from django.shortcuts import render, redirect, get_object_or_404
from contest.forms import Team_Form, Team_Edit, Team_Delete_Members, Team_Add_Members
from django.http import HttpResponseRedirect
from article.models import Article
from userregistration.models import CustomUser
from userregistration.models import CustomUserManager
from contest.models import Team, Invite, Contest
from django.contrib.auth import get_user_model
from django.contrib.sites.models import get_current_site
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.contrib import messages


User = get_user_model()
# Create your views here.

def index(request):
    url = request.path.split('/')[1]
    article_list = Article.objects.all().filter(contest__url = url).order_by("-created_at")
    context = {'article_list' : article_list, 
               }    
    return render(request, 'contest/index.html', context)

def is_on_team(request):
    pass

# @login_required
def registration(request):
    '''
    TODO: Ch3ck if you already have a team. 
    '''
    if request.method == 'POST' and is_member_of_team(request): 
        messages.warning(request, 'Unfortunately you can only be part of one team for this contest. :( ')
    
    elif is_member_of_team(request):
        messages.info(request, 'Unfortunately you can only be part of one team for this contest. :( ')
    
    elif request.method == 'POST': # If the form has been submitted...
        # teamform is defined in openshif.contest.models
        form = Team_Form(request.POST) # A form bound to the POST data
        
        if form.is_valid(): # All validation rules pass
            #new_team = form.save(commit=False)
            email_one = form.cleaned_data['email_one']
            email_two = form.cleaned_data['email_two'] 
            
            print request.user.email
            
            '''
            We need to check if the emails are equal. You should not be able to use to equal emails.
            '''
            if (email_one == email_two):
                messages.error(request, 'Please do not use equal emails')                
            
            #checks if you are trying to add yourself. It is no legal. 
            elif request.user.email == email_one or request.user.email == email_two:
                messages.error(request, 'Please do not fill inn your own email. You will be added as leader by default.')
                pass                            
                
            else: # if the emails do not equal each other
                    
                try: 
                    url = request.path.split('/')[1]
                except ObjectDoesNotExist as e: 
                    raise Http404
                
                try: 
                    current_contest = Contest.objects.get(url = url)
                except ObjectDoesNotExist as e: 
                    raise Http404
                
                team = Team.objects.create(name=form.cleaned_data['name'], onsite=form.cleaned_data['onsite'], 
                                           offsite=form.cleaned_data['offsite'], contest = current_contest, leader = request.user)
                team.members.add(request.user)
                '''
                Clearifaction: We have decided to add the current user as a leader AND as a member. 
                '''                
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
                messages.success(request, "You are now ready to compete in the compititon")
                
                return render(request, 'registerForContest/registrationComplete.html')
                #end else
            return render(request, 'registerForContest/registration.html', {
                    'form': form,
                    })

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

AUTHOR: Haakon, Tino, Filip

'''
@login_required
def teamProfil(request):    
    user = request.user
    url = request.path.split('/')[1]

    site = get_current_site(request)

    # Need to give error if you dont have team (link to register team page)
    team = Team.objects.filter(members__id = user.id)
    if team.count() > 0:
        team = team[0]
    else:
        team = None
         
    # TODO: Only visible to Team leaders
    if request.method == 'POST':
        addMemberForm = Team_Add_Members(request.POST)
        if addMemberForm.is_valid():
            email = addMemberForm.cleaned_data['email']
            if Team.objects.get(pk=team.id).members.count() < 3:  #TODO: Fix hard code      
                invite = Invite.objects.create_invite(email, team, url, site)
                invite.save()
                messages.success(request, 'Email has been sent to: ' + email)
            else:   
                messages.error(request, 'You already have the maximum number of members')
    else:        
        addMemberForm = Team_Add_Members()
        
    context = {'team':team, 'addMemberForm' : addMemberForm,}
    return render(request, 'contest/team.html', context)

'''
AUTHOR: Tino, Filip
'''

#Haakon
def is_member_of_team(request):
    team = Team.objects.filter(members__id = request.user.id)
    if team.count() > 0:
        return team[0]
    else:
        team = False


@login_required
def editTeamProfil(request):
    print("You are now in Edit Team Profil View")
    user = request.user
    url = request.path.split('/')[1]
    # Get the team or 404
    instance = get_object_or_404(Team, members__in=CustomUser.objects.filter(pk=user.id))
    # make a new form, with the instance as its model
    editForm = Team_Edit(None, instance = instance)
    deleteForm = Team_Delete_Members(None, instance = instance)
    if request.method == 'POST':
        if 'edit' in request.POST:
            editForm = Team_Edit(request.POST, instance = instance)
            if editForm.is_valid():
                messages.success(request, 'Profile details updated.')
                editForm.save()
        if 'deletebutton' in request.POST:
            deleteForm = Team_Delete_Members(request.POST, instance = instance)
            if deleteForm.is_valid():
                if deleteForm.save():
                    messages.success(request, 'Members updated.')
                else:
                    messages.error(request, 'Something went wrong')
                       
    return render(request, 'contest/editTeam.html', {
        'editForm': editForm,
        'deleteForm': deleteForm,
        'team': instance,
    })

