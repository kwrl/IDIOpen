from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, Http404
from contest.views import get_current_contest
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

def submission_problem(request, problemID):
    #TODO: maybe a nicer url than numeric ID
    con = get_current_contest(request)
    
    # Raise 404 if contest hasn't begun or has ended
    if not contest_begin(con):
        raise Http404    
    
    if contest_end(con):
        messages.warning(request, 'The contest has ended, you are not able to upload any more submissions.')
   
    #TODO: Only leader can upload check    
    problem = get_object_or_404(Problem.objects.filter(pk=problemID))
    user = request.user
    team = Team.objects.filter(contest=con).get(members__id = user.id)
    submission = Submission.objects.filter(team=team).filter(problem=problemID).order_by('date_uploaded')
    tries = len(submission)
    
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
        if contest_end(con):
            messages.error(request, 'You can\'t upload any more files after the contest has ended')
        elif form.is_valid():
            form.save()
    
#    pdb.set_trace()
    if is_problem_solved(team, problemID): 
        messages.success(request, 'This problem is solved!')
            
    form = SubmissionForm(instance=submission);
      
    
    
    context = {
             'problem' : problem,
             'submission' : submission,
             'submission_form' : form,
             'tries':tries,
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
    if not contest_begin(con):
        raise Http404    
    
    if not user.is_authenticated():
        return redirect('login', con.url)

    if contest_end(con):
        messages.warning(request, 'The contest has ended, you are not able to upload any more submissions.')
    
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