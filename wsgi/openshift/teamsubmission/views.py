from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, Http404
from contest.views import get_current_contest, is_leader, is_member_of_team
from contest.models import Team
from execution.models import Problem

from .models import Submission
from .forms import SubmissionForm

from itertools import groupby, imap, izip_longest
from operator import itemgetter
from django.contrib import messages
from contest.views import contest_begin, contest_end

def is_problem_solved(team, problemID):
    submission = Submission.objects.filter(team=team).filter(problem=problemID).filter(solved_problem = True)
    if submission:
        return True
    return False

#Login required
def submission_problem(request, problemID):
    #TODO: maybe a nicer url than numeric ID
    con = get_current_contest(request)
    user = request.user
    if not user.is_authenticated():
        return redirect('login', con.url)
    # Raise 404 if contest hasn't begun or has ended, and if user is not member of team
    if not contest_begin(request) or not is_member_of_team(request, con):
        raise Http404    
    if contest_end(request):
        messages.warning(request, 'The contest has ended, you are not able to upload any more submissions.')
   
    #TODO: Only leader can upload check    
    problem = get_object_or_404(Problem.objects.filter(pk=problemID))
    user = request.user
    team = Team.objects.filter(contest=con).get(members__id = user.id)
    submission = Submission.objects.filter(team=team).filter(problem=problemID).order_by('-date_uploaded')
    tries = len(submission)
    
    
    score = Submission.objects.get_problem_score(team, problem, con)

    
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
        
        elif is_leader(request, con):
            if form.is_valid():
                form.save()
                form = SubmissionForm(instance=submission);
        else:
            messages.error(request, 'You have to be the leader of a team to upload submissions')
    else:
        form = SubmissionForm(instance=submission);
    
    context = {
             'problem' : problem,
             'submission' : submission,
             'submission_form' : form,
             'tries':tries,
             'score' : score,
              }
    
    return render(request,
                  'problemdescription.html',
                  context,
                  )

#Login required
def submission_view(request):
    user = request.user
    con = get_current_contest(request)
    
    # Raise 404 if contest hasn't begun or contest has ended
    if not contest_begin(request) or not is_member_of_team(request, con):
        raise Http404    
    
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
    problems = statistics[0][4:]
    
    context = {
               'contest' : contest,
               'statistics' : statistics,
               'problems' : problems
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
                        submission.date_uploaded.strftime('%H:%M:%S')
        self.problem = problem 
# EOF