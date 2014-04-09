from django.shortcuts import render, get_object_or_404
from contest.views import get_current_contest
from contest.models import Team
from execution.models import Problem

from .models import Submission
from .forms import SubmissionForm

from itertools import groupby, imap, izip_longest
from operator import itemgetter
from django.contrib import messages

def submission_problem(request, problemID):
    #TODO: maybe a nicer url than numeric ID
    
    problem = get_object_or_404(Problem.objects.filter(pk=problemID))
    user = request.user
    con = get_current_contest(request)
    team = Team.objects.filter(contest=con).get(members__id = user.id)
    
    submission = Submission.objects.filter(team=team).filter(problem=problemID).order_by('date_uploaded')
            
    if len(submission.values_list()) > 0:
        submission = submission[0]
        problem = submission.problem
    else:
        submission = Submission()
        submission.problem = problem
        submission.team = team
    
    if request.method == "POST":
        form = SubmissionForm(request.POST, request.FILES,
                               instance=submission)
        if form.is_valid():
            form.save()
            
    form = SubmissionForm(instance=submission);  
    
    context = {
             'problem' : problem,
             'submission' : submission,
             'submission_form' : form,
              }
    
    return render(request,
                  'problemdescription.html',
                  context,
                  )


#Login required
def submission_view(request):
    user = request.user
    con = get_current_contest(request)
    
    team = Team.objects.filter(contest=con).filter(members__id = user.id)
    problems = Problem.objects.filter(contest=con)
    submissions = Submission.objects.filter(team=team).order_by('date_uploaded')
    # Get only one submission per problem. 
    # The submission is the first one returned, as per date_uploaded
    ret_submissions = map(next, imap(itemgetter(1),
                          groupby(submissions, lambda x:x.problem)))
        
    listProbSub = [SubJoinProb(sub, prob) 
                   for (sub, prob) in izip_longest(ret_submissions, problems)]
    
    
    context = {
               'problems' : problems,
               'submissions' : submissions,
               'prob_sub': listProbSub,
               }    
    return render(request, 'submission_home.html', context)

def highscore_view(request):
    contest = get_current_contest(request)
    scores = Submission.objects.get_highscore(contest)
    
    context = {
               'contest' : contest,
               'scores' : scores,
               }
    return render(request, 'highscore.html', context)

class SubJoinProb(object):
    def __init__(self, submission, problem):
        if submission is not None:
                self.submission = submission
                self.submission.submission = \
                    str(submission.submission).split('/')[-1]
                self.submission.date_uploaded = \
                        submission.date_uploaded.strftime('%H:%M:%S')
        self.problem = problem 
        
# EOF