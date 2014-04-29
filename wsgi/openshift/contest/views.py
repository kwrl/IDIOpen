#coding:utf-8
from django.shortcuts import render, redirect, get_object_or_404
from .forms import Team_Form, Team_Edit, Team_Add_Members
from openshift.article.models import Article
from openshift.userregistration.models import CustomUser
from .models import Team, Invite, Contest
from django.contrib.auth import get_user_model
from django.contrib.sites.models import get_current_site
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.contrib import messages
from openshift.helpFunctions import views as helpViews

import datetime;
from django.utils import timezone;

# Create your views here.

def index(request):
    url = get_current_url(request)

    '''
    article_urgent = Article.objects.all().filter(contest__url = url, is_urgent = True).order_by("-created_at")
    if not article_urgent:
        article_urgent = Article.objects.all().order_by("-created_at")[:1].get()
    '''
    article_list = Article.objects.all().filter(contest__url = url).exclude(visible_article_list = False).order_by("-is_urgent","-created_at")[:7]


    context = {'article_list' : article_list,
               }
    return render(request, 'contest/index.html', context)

def get_current_url(request):
    try:
        url = request.path.split('/')[1]
    except ObjectDoesNotExist as e:
        raise Http404
    return url;

def get_current_contest(request):
    try:
        current_contest = Contest.objects.get(url = get_current_url(request))
    except ObjectDoesNotExist as e:
        raise Http404
    return current_contest;

def getTodayDate(request):
    con = get_current_contest(request);
    return timezone.make_aware(datetime.datetime.now(),
                               timezone.get_default_timezone());

'''
AUTHOR: Tino, Filip
'''
#===============================================================================
# Check if user is Team leader
#===============================================================================
def is_leader(request, contest):
    leader_team = Team.objects.filter(contest=contest).get(members__id = request.user.id)
    if leader_team.leader.id == request.user.id and leader_team.pk == helpViews.get_team(request).pk:
        return True
    else:
        return False

#===============================================================================
# Check if user is on a team
#===============================================================================
def is_member_of_team(request, contest):
    team = Team.objects.filter(contest=contest).filter(members__id = request.user.id)
    if team.count() > 0:
        return team[0]
    else:
        team = False


# @login_required
def registration(request):
    '''
    TODO: Ch3ck if you already have a team.
    Done?
    '''
    if not request.user.is_authenticated():
        return render(request, 'registerForContest/requireLogin.html')
    
    con = get_current_contest(request);

    if not con.isRegOpen():
        messages.error(request, 'Registration is now closed');
        request.GET = {}; request.POST = {};
        tf = Team_Form();
        tf.disable_fields();
        return render(request, 'registerForContest/registration.html', {
                    'form': tf,
                    });
    if request.method == 'POST' and is_member_of_team(request, con):
        messages.warning(request, 'Unfortunately you can only be part of one team for this contest. :( ')

    elif is_member_of_team(request, con):
        messages.info(request, 'Unfortunately you can only be part of one team for this contest. :( ')

    elif request.method == 'POST': # If the form has been submitted...
        # teamform is defined in openshif.contest.models
        form = Team_Form(request.POST) # A form bound to the POST data

        if form.is_valid(): # All validation rules pass
            #new_team = form.save(commit=False)
            email_one = form.cleaned_data['member_one']
            email_two = form.cleaned_data['member_two']

            '''
            We need to check if the emails are equal. You should not be able to use to equal emails.
            '''
            if (email_one == email_two and email_one != "" and email_two != ""):
                messages.error(request, 'Please do not use equal emails')

            #checks if you are trying to add yourself. It is no legal.
            elif request.user.email == email_one or request.user.email == email_two:
                if(request.user.email == ""):
                    pass
                messages.warning(request, 'Please do not fill inn your own email. You will be added as leader by default.')
                pass

            else: # if the emails do not equal each other

                # Removes whitespace from name and offsite
                name = form.cleaned_data['name'].strip()
                offsite = form.cleaned_data['offsite'].strip()
                team = Team.objects.create(name=name, onsite=form.cleaned_data['onsite'],
                                           offsite=offsite, contest = con, leader = request.user)
                team.members.add(request.user)
                '''
                Clarifaction: We have decided to add the current user as a leader AND as a member.
                '''
                '''
                TODO:  This should be a loop, looping over the number allowed members. For now this will be OK.
                '''

                site = get_current_site(request)

                if email_one:
                    invite_1 =Invite.objects.create_invite(email = email_one, team=team, url=con.url, site=site); # adding "user" (a.k.a the email) to invite list.
                    invite_1.save()

                if email_two:
                    invite_2 = Invite.objects.create_invite(email = email_two, team=team, url=con.url, site=site); # adding "user" (a.k.a the email) to invite list.
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

#===============================================================================
# Checks if contest has begun
#===============================================================================
def contest_begin(request):
    try:
        contest = get_current_contest(request)
        startDate = contest.start_date
        dateToday = timezone.now()
        if (dateToday >= startDate):
            has_started = True
        else:
            has_started = False
    except ObjectDoesNotExist as e:
        raise Http404
    return has_started
#===============================================================================
# Checks if contest has ended
#===============================================================================
def contest_end(request):
    try:
        contest = get_current_contest(request)
        endDate = contest.end_date
        dateToday = timezone.now()
        if (dateToday <= endDate):
            has_ended = False
        else:
            has_ended = True
    except ObjectDoesNotExist as e:
        raise Http404
    return has_ended
'''
AUTHOR: Tino, Tino, Filip
'''
#@login_required
def team_profile(request):
    user = request.user
    con = get_current_contest(request);
    if not user.is_authenticated():
        return redirect('login', con.url)

    site = get_current_site(request)
    # Need to give error if you dont have team (link to register team page)
    team = Team.objects.filter(contest=con).filter(members__id = user.id)
    # If you have a team
    if team.count() > 0:
        team = team[0]
        invites = Invite.objects.filter(team=team).filter(is_member = False)

        contest_started = contest_begin(request)
        # If you are the leader
        leader = is_leader(request,con)

        # Create empty addMemberForm
        addMemberForm = Team_Add_Members()

        # If the competition has started
        if (contest_started):
            context = {'team':team,
                       'invites' : invites,
                       'addMemberForm' : addMemberForm,
                        'is_leader' : leader,
                       'contest_started' : contest_started,
                       }
            return render(request, 'contest/team.html', context)
        # If you are the leader
        leader = is_leader(request,con)
        if leader:
            if request.method == 'POST':
                if not contest_started:
                    addMemberForm = Team_Add_Members(request.POST)
                    if addMemberForm.is_valid():
                        email = addMemberForm.cleaned_data['email']
                        if Team.objects.get(pk=team.id).members.count() < 3:  #TODO: Fix hard code
                            invite = Invite.objects.create_invite(email, team, con.url, site)
                            invite.save()
                            messages.success(request, 'Email has been sent to: ' + email)
                        else:
                            messages.error(request, 'You already have the maximum number of members')
                else:
                    messages.error(request, 'Sorry, you can\'t add members after the contest has started')
            # send team, addMemberForm and is_leader with context
            context = {'team':team,
                       'addMemberForm' : addMemberForm,
                       'is_leader' : leader,
                       'invites' : invites,
                       }
        # If user is not leader, send context without addMemberForm
        else:
            context = {'team':team,
                       'is_leader' : leader,
                       'invites' : invites,
                       }
    # If you don't have team, send an empty context
    else:
        context = {}

    return render(request, 'contest/team.html', context)


#===============================================================================
# For when a contestant wants to leave a team
#===============================================================================
def leave_team(request):
    user = request.user
    con = get_current_contest(request)
    is_RegOpen = con.isRegOpen()
    if request.method == 'POST' and contest_begin(request):
        messages.error(request, 'Sorry, you can\'t leave team after registration is closed')
    elif request.method == 'POST':
        if is_RegOpen:
            if is_leader(request, con): # If leader, delete the team
                team = Team.objects.filter(contest=con).get(members__id = request.user.id)
                if team.members.all().count() > 1: # If member count is > 1
                    messages.error(request, 'You need to transfer leadership before you can leave the team.')
                else:
                    team.delete()
            else: # else delete the member from the team
                team = Team.objects.filter(contest=con).get(members__id = request.user.id)
                team.members.remove(user.id)
        else:
            messages.error(request, 'Sorry, you can\'t leave team after registration is closed')

    return redirect('team_profile', con.url)

#===============================================================================
#For when a leader wants to edit the team
#===============================================================================
#@login_required
def editTeam(request):
    user = request.user
    url = get_current_url(request)
    con = get_current_contest(request)

    if not user.is_authenticated():
        return redirect('login', url)

    if (contest_begin(request)):
        raise Http404()
    # Get the team or 404
    queryset = Team.objects.filter(contest=con).filter(members__in = [user])
    instance = get_object_or_404(queryset)#team
    # make a new form, with the instance as its model
    form = Team_Edit(None, instance = instance)
    # Need to be leader to edit a profile
    if is_leader(request, con):
        if request.method == 'POST':
            form = Team_Edit(request.POST, instance = instance)
            if form.is_valid():
                messages.success(request, 'Profile details updated.')
                form.save()
                return redirect('team_profile', url)
    else:
        messages.error(request, 'You are not the team leader')

    return render(request, 'contest/editTeam.html', {
        'form': form,
        'team': instance,
    })


def view_teams(request):
    try:
        team_list = Team.objects.filter(contest = get_current_contest(request))
    except ObjectDoesNotExist as e:
        messages.info(request, "Something went wrong :(")

    if len(team_list) < 1:
        messages.info(request, "There are current no team registered for this contest. Why not be the first?")

    return render(request, 'viewTeams/viewTeams.html',{
                  'team_list': team_list,
                  'number_of_teams': len(team_list)
                  })

'''
TODO: You can delete member after
'''
def deleteMember(request, member_id):
    user = request.user
    url = request.path.split('/')[1]
    con = get_current_contest(request)
    if is_leader(request, con):
        queryset = Team.objects.filter(contest=con).filter(members__in = [user])
        team = get_object_or_404(queryset)
        member = CustomUser.objects.get(pk=member_id)
        team.members.remove(member)
        messages.success(request, 'Member deleted')
    else:
        messages.warning(request, 'Only the leader can delete members')

    return redirect('team_profile', url)


#What are you doing down here? POEM TIME!!!!1
# Roses are red
# Violets are blue
# I am a Dragon
# And i love U2
def cage_me(request):
    return render(request,'Cage/cage.html')

