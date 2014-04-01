from django.shortcuts import render
from contest.views import get_current_contest
from contest.models import Team
from execution.models import Problem
from .models import Submission
from itertools import groupby, imap
from operator import itemgetter

def submission_problem(request, problemID):
    #TODO: maybe a nicer url than numeric ID
    user = request.user
    problem = Problem.objects.filter(pk=problemID)
    con = get_current_contest(request)
    team = Team.objects.filter(contest=con).filter(members__id = user.id)

    submission = Submission.objects.filter(team=team).order_by('date_uploaded')
    if len(submission) > 0:
        submission = submission[0]
    else:
        submission = None
        
    
    context = {
             'problem' : problem,
             'submission' : submission,
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
    # Get only on submission per problem. 
    # The submission is the first one returned, as per date_uploaded
    ret_submissions = map(next, imap(itemgetter(1),
                                groupby(submissions, lambda x:x.problem)))
   
    listProbSub = [SubJoinProb(sub, prob) 
                   for (sub, prob) in zip(ret_submissions, problems)]
    
    context = {
               'problems' : problems,
               'submissions' : submissions,
               'prob_sub': listProbSub,
               }    
    return render(request, 'submission_home.html', context)

class SubJoinProb(object):
    def __init__(self, submission, problem):
        self.submission = submission
        self.submission.submission = \
            str(submission.submission).split('/')[-1]
        self.submission.date_uploaded = \
                submission.date_uploaded.strftime('%H:%M:%S')
        self.problem = problem 
        
# EOF