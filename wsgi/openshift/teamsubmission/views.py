""" Views related to submissions
"""
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, Http404
from django.utils.timezone import utc

from openshift.contest.views import contest_begin, contest_end, get_current_contest, is_member_of_team
from openshift.contest.models import Team
from openshift.execution.models import Problem
from openshift.helpFunctions.views import get_score
from .models import Submission
from .forms import SubmissionForm

import datetime
from datetime import timedelta
from collections import defaultdict
from django.core.exceptions import ObjectDoesNotExist

CLOSE_TIME = 1 #Hour

def get_problem_score_tries(team, problem, contest):
    prob_subs = Submission.objects.filter(team=team, problem=problem)
    incorrect_counts = 0
    valid_sub = None
    sub = None
    for sub in prob_subs:
        if sub.solved_problem:
            valid_sub = sub
        else:
            incorrect_counts += 1
    _, score = get_score(valid_sub, incorrect_counts, contest)
    if valid_sub: 
        incorrect_counts +=1
    return score, incorrect_counts

def is_problem_solved(team, problemID):
    submission = Submission.objects.filter(team=team).filter(problem=problemID).filter(solved_problem = True)
    if submission:
        return True
    return False

'''
AUTHOR: Tino, Filip
'''
#===============================================================================
# Check if user is Team leader
#===============================================================================
def is_leader(request, contest):
    team = Team.objects.filter(contest=contest).get(members__id = request.user.id)
    if team.leader.id == request.user.id:
        return True
    else:
        return False


#View for uploading submissions to a problem
def submission_problem(request, problemID):
	'''
	The view for uploading submission and reviewing the status of a team's
	latest submission. By default this view lets teams upload submission,
	once the team has uploaded a valid submission they are no longer able 
	to upload any more submission and the view simply tells the user that
	the problem has been solved, awarding the team x points.
	'''

    #TODO: maybe a nicer url than numeric ID
    contest = get_current_contest(request)
    user = request.user
            
    if not user.is_authenticated():
        return redirect('login', contest.url)
    
    if not user.is_staff:
        # Raise 404 if contest hasn't begun or has ended, and if user is not member of team
        if not contest_begin(request) or not is_member_of_team(request, contest):
            raise Http404
        if contest_end(request):
            messages.warning(request, 'The contest has ended, you are not able to upload any more submissions.')
    
        if not is_leader(request, contest):
            messages.warning(request, 'Only leader can upload a solution')
    
    else:
        messages.warning(request, 'pssst: You are now logged in with a staf user')
        

    #TODO: Only leader can upload check
    problem = get_object_or_404(Problem.objects.filter(pk=problemID)) 
    team = Team.objects.filter(contest=contest).get(members__id = user.id)
    submission = Submission.objects.filter(team=team).filter(problem=problemID).order_by('date_uploaded')
    prob_sub_dict = dict() #Was is das?

    if len(submission.values_list()) > 0:
        submission = submission[0]
        problem = submission.problem
    else:
        submission = Submission()
        submission.problem = problem
        submission.team = team
    
    ''''
    Does not look good|
    if is_problem_solved(team, problemID):
        messages.success(request, 'This problem is solved!')
    '''
    
    
    if request.method == "POST":
        form = SubmissionForm(request.POST, request.FILES,
                               instance=submission)
        
        if not request.FILES:
            messages.error(request, 'You need to choose a file to upload')

        elif contest_end(request):
            messages.error(request, 'You can\'t upload any more files after the contest has ended')
        
        elif (submission.status != submission.EVALUATED and submission.status != submission.NOTSET):
            messages.info(request, 'Please wait. Only one submisison at a time')
        
        elif is_leader(request, contest) or user.is_staff:
            if form.is_valid():
                form.save()
                return redirect('submission_problem', contest.url, problemID)

        else:
            messages.error(request, 'You have to be the leader of a team to upload submissions')
        
    elif not submission.solved_problem:
        form = SubmissionForm(instance=submission);
    else:
        form = None

    score, tries = get_problem_score_tries(team, problem, contest)
    context = {
             'problem' : problem,
             'submission' : submission,
             'submission_form' : form,
             'tries': tries,
             'score' : score,
              }

    return render(request,
                  'problemdescription.html',
                  context,
                  )

#Login required
def submission_view(request):
	'''
	This is what is the view used to serve what is usually referred to
	as the contest page. The contest page consists of the list of problems
	available in the contest. Each of the problems are marked with whether
	or not they are solved, and prints the feedback of the latest attempt
	made by the team viewing the page.
	'''
    user = request.user
    contest = get_current_contest(request)

    if not user.is_authenticated():
        messages.error(request, 'You have to be logged in in order to view the contest page')
        return redirect('login', contest.url)
    
    if not user.is_staff:
        if not is_member_of_team(request, contest):
            messages.error(request, 'Please register a team to participate')
            return redirect('team_profile', contest.url)
    
        # Raise 404 if contest hasn't begun or contest has ended
        if not contest_begin(request):
            messages.error(request, 'Contest has not yet started')
            return redirect('contest_list', contest.url)
    
        if contest_end(request):
            messages.warning(request, 'The contest has ended, you are not able to upload any more submissions.')
    
    else:
        team = Team.objects.filter(contest=contest, members__id = user.id)
        if  team:
            messages.warning(request, 'pssst: You are now logged in with a staf user, remember to delete your team before contest start') 
        else: 
            messages.warning(request, 'pssst: You are now logged in with a staf user. you need a team in order to test. Create a team and remember to delete it before contest start!')
    
    team = Team.objects.filter(contest=contest, members__id = user.id)
    problems = Problem.objects.filter(contest=contest)
    prob_sub_dict = dict()

    """ Get the latest submission for each problem
    """
    prob_attempts = defaultdict( int )
    for sub in Submission.objects.filter(team=team):
        """ Get the amount of attempts for a problem
        """
        prob_attempts[sub.problem] += 1

        """ we're trying for latest date"""
        if sub.problem in prob_sub_dict:
            old_sub = prob_sub_dict[sub.problem]
            # Replace with better
            if old_sub.date_uploaded < sub.date_uploaded:
                prob_sub_dict[sub.problem] = sub
        else:
            # Insert new
            prob_sub_dict[sub.problem] = sub


    listProbSub = []
    team_score = 0
    for prob in problems:
        sub = None
        if prob in prob_sub_dict:
            sub= prob_sub_dict[prob]
            incorrect_tries = prob_attempts[prob]
            if sub.solved_problem and incorrect_tries > 0:
                incorrect_tries -= 1
            team_score += get_score(sub, incorrect_tries , contest)[1]
        listProbSub.append(SubJoinProb(sub, prob,
                         get_problem_score_tries(team, prob, contest)[0]))

    """
    For testing:
    SELECT ts.submission, ts.date_uploaded, ep.title, ts.solved_problem
    FROM teamsubmission_submission AS ts, execution_problem AS ep
    WHERE ts.problem_id = ep.id AND ts.team_id = 7 ;
    """

    context = {
               'prob_sub': listProbSub,
               'team_score' : team_score,
               }

    return render(request, 'submission_home.html', context)

def highscore_view(request, sort_res="all"):
	'''
	This view calculates and renders the highscore list.
	During the last hour of the contest this list will no
	longer be available. Privileged users will have access
	to a more thorough list available in the admin panel. 
	'''
    # sort res can say offsite of onsite or student or pro
    contest = get_current_contest(request)

    highscore = Submission.objects.get_highscore(contest, sort_res)
    problems = Problem.objects.all()
    
    context = {
               'contest' : contest,
               #'statistics' : teams,
               'highscore' : highscore,
               'problems' : problems,
               'freeze' : show_contest(contest),
               'locations' : ["onsite", "offsite"],
               'team_types' : ["student", "pro"],
               'sort_res' : sort_res,
               }
    
    return render(request, 'highscore.html', context)

class SubJoinProb(object):
    def __init__(self, submission, problem, score):
        if submission is not None:
            self.score = score
            self.submission = submission
            self.submission.submission = \
                str(submission.submission).split('/')[-1]
            self.submission.date_uploaded = \
                submission.date_uploaded
        self.problem = problem
'''
Returs false if highscore should be hidden
TODO: This could be maybe be a templatetag? 
'''
def show_contest(contest):    
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    day = datetime.date.today()
    
    #We subtract on hour    
    close_time_first = contest.end_date-timedelta(hours=CLOSE_TIME)
    close_time_completed = contest.end_date
    
    if (now > close_time_first and now < close_time_completed):
        return False
    else:
        return True

# END OF LIFE

