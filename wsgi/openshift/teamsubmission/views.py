from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, Http404
from openshift.contest.views import get_current_contest, is_leader, is_member_of_team
from openshift.contest.models import Team
from openshift.execution.models import Problem

from .models import Submission
from .forms import SubmissionForm

from itertools import groupby, imap, izip_longest
from operator import itemgetter
from django.contrib import messages
from openshift.contest.views import contest_begin, contest_end

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
    #TODO: maybe a nicer url than numeric ID
    contest = get_current_contest(request)
    user = request.user
    if not user.is_authenticated():
        return redirect('login', contest.url)
    # Raise 404 if contest hasn't begun or has ended, and if user is not member of team
    if not contest_begin(request) or not is_member_of_team(request, contest):
        raise Http404    
    if contest_end(request):
        messages.warning(request, 'The contest has ended, you are not able to upload any more submissions.')
   
    if not is_leader(request, contest):
        messages.warning(request, 'Only leader can upload a solution')
   
    #TODO: Only leader can upload check    
    problem = get_object_or_404(Problem.objects.filter(pk=problemID))
    user = request.user
    team = Team.objects.filter(contest=contest).get(members__id = user.id)
    submission = Submission.objects.filter(team=team).filter(problem=problemID).order_by('-date_uploaded')
    tries = len(submission)
    
    
    if len(submission.values_list()) > 0:
        submission = submission[0]
        problem = submission.problem
    
    else:
        submission = Submission()
        submission.problem = problem
        submission.team = team
    
    '''
    Does not look good
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
        
        elif is_leader(request, contest):
            if form.is_valid():
                form.save()
                return redirect('submission_problem', contest.url, problemID)
        else:
            messages.error(request, 'You have to be the leader of a team to upload submissions')
    elif not submission.solved_problem:
        form = SubmissionForm(instance=submission);
    else:
        form = None
    
    score = Submission.objects.get_problem_score(team, problem, contest)
    context = {
             'problem' : problem,
             'submission' : submission,
             'submission_form' : form,
             'tries':tries,
             'score' : score[0],
              }
    
    return render(request,
                  'problemdescription.html',
                  context,
                  )

#Login required
def submission_view(request):
    user = request.user
    con = get_current_contest(request)
    
    if not user.is_authenticated():
        messages.error(request, 'You have to be logged in in order to view the contest page')
        return redirect('login', con.url)
    
    
    if not is_member_of_team(request, con):
        messages.error(request, 'Please register a team to participate')
        return redirect('team_profile', con.url)
        
    
    # Raise 404 if contest hasn't begun or contest has ended
    if not contest_begin(request):
        messages.error(request, 'Contest has not yet started')
        return redirect('contest_list', con.url)
        
    
    
    if not user.is_authenticated():
        return redirect('login', con.url)

    if contest_end(request):
        messages.warning(request, 'The contest has ended, you are not able to upload any more submissions.')
    
    team = Team.objects.filter(contest=con).filter(members__id = user.id)
    problems = Problem.objects.filter(contest=con).order_by('title')
    submissions = Submission.objects.filter(team=team).order_by('-date_uploaded').order_by('problem')
    
    new_dict = dict()
    listProbSub = []
    
    for sub in submissions:
        new_dict[sub.problem] = sub
    for prob in problems:
        if prob in new_dict:
            sub = new_dict[prob]
        else:
            sub = None
        listProbSub.append((SubJoinProb(sub, prob, 
                Submission.objects.get_problem_score(team, prob, con)))
        )
    
    context = {
               'prob_sub': listProbSub,
               }    
    
    return render(request, 'submission_home.html', context)

def highscore_view(request):
    contest = get_current_contest(request)
    statistics = Submission.objects.get_highscore(contest)
    problems = []
    if statistics:
        problems = statistics[0][8:]
    
    context = {
               'contest' : contest,
               'statistics' : statistics,
               'problems' : problems
               }
    return render(request, 'highscore.html', context)

class SubJoinProb(object):
    def __init__(self, submission, problem, score):
        if submission is not None:
                self.score = score[0]
                self.submission = submission
                self.submission.submission = \
                    str(submission.submission).split('/')[-1]
                self.submission.date_uploaded = \
                    submission.date_uploaded.strftime('%H:%M:%S')
        self.problem = problem 

# END OF LIFE
