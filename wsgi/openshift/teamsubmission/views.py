from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, Http404
from openshift.contest.views import get_current_contest, is_member_of_team
from openshift.contest.models import Team
from openshift.execution.models import Problem

from .models import Submission
from .forms import SubmissionForm

from django.contrib import messages
from openshift.contest.views import contest_begin, contest_end
from openshift.helpFunctions.views import get_score

import datetime
from datetime import timedelta
from django.utils.timezone import utc
CLOSE_TIME = 1 #Hour

def get_problem_score(team, problem, contest):
    prob_subs = Submission.objects.filter(team=team, problem=problem)
    incorrect_counts = 0
    valid_sub = None
    sub = None
    for sub in prob_subs:
        if sub.solved_problem:
            sub = sub
        else:
            incorrect_counts += 1
    _, score = get_score(sub, incorrect_counts, contest)
    return score

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
    submission = Submission.objects.filter(team=team).filter(problem=problemID)
    prob_sub_dict = dict()

    # get_team_score()

    """ Get the latest submission for each problem
    """
    for sub in Submission.objects.filter(team=team):
        if sub.problem in prob_sub_dict:
            old_sub = prob_sub_dict[sub.problem]
            # Replace with better
            if old_sub.date_uploaded < sub.date_uploaded:
                prob_sub_dict[sub.problem] = sub
        else:
            # Insert new
            prob_sub_dict[sub.problem] = sub


    listProbSub = []
    for prob in problems:
        sub = None
        if prob in prob_sub_dict:
            sub= prob_sub_dict[prob]
        listProbSub.append(SubJoinProb(sub, prob,
                         get_problem_score(team, prob, con)))

    """
    For testing:
    SELECT ts.submission, ts.date_uploaded, ep.title, ts.solved_problem
    FROM teamsubmission_submission AS ts, execution_problem AS ep
    WHERE ts.problem_id = ep.id AND ts.team_id = 7 ;
    """

    context = {
               'prob_sub': listProbSub,
               'team_score' : Submission.objects.get_team_score(team[0], con, problems)[1]
               }

    return render(request, 'submission_home.html', context)

def highscore_view(request, sort_res="all"):
    contest = get_current_contest(request)

    highscore = Submission.objects.get_highscore(contest)
    problems = Problem.objects.all()
        
    # problems = []
    # teams = []    
    # if statistics:
    #     problems = Problem.objects.filter(contest=contest)
    #     if sort_res == "all":
    #         teams = statistics
    #     else:
    #         for team in statistics:
    #             if sort_res == "offsite" and team[2]:
    #                 teams.append(team)
    #             elif sort_res == "onsite" and not team[2]:
    #                 teams.append(team)
    #             elif sort_res == "student" and team[6] <= 6:
    #                 teams.append(team)
    #             elif sort_res == "pro" and team[6] > 6:
    #                 teams.append(team)
    # 
    # 
    #import ipdb; ipdb.set_trace()
    context = {
               'contest' : contest,
               #'statistics' : teams,
               'highscore' : highscore,
               'problems' : problems,
               'freeze' : show_contest(contest)
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

