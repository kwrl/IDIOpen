""" The views for the balloon overview table
"""

from django.contrib import admin
from django.db import models
from django.shortcuts import render, HttpResponse
from django.conf.urls import url, patterns

from openshift.contest.models import Contest
from openshift.helpFunctions.views import get_most_plausible_contest, in_contest
from openshift.teamsubmission.models import Submission
from openshift.balloon.models import BalloonStatus, balloon_view
from openshift.balloon.forms import BalloonSubmissionForm

class judge_view_admin(admin.ModelAdmin):
    # FIXME
    """ Temporary solution to get a view connected iSubmissionn admin site
    """

    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request):
        return False

    def get_urls(self):
        urls = super(judge_view_admin, self).get_urls()
        urls = [urls[0], ]
        my_urls = patterns('',
           url(r'^$', admin.site.admin_view(balloon_home)),
           url(r'^con(?P<contest_pk>[0-9]+)$',
               admin.site.admin_view(balloon_home)),
        )
        return my_urls + urls

class BalloonView(object):
    def __init__(self, submission, timestamp=None):
        self.submission = submission
        self.timestamp = timestamp

def _get_table_lists(contest):
    balloons = BalloonStatus.objects.all()
    balloon_subs = dict([(ball.submission.pk, ball.timestamp) \
                            for ball in balloons \
                                if in_contest(ball.submission, contest)])

    submissions = Submission.objects.filter(team__onsite = 'True')\
                           .filter(solved_problem = 'True')

    if submissions.count() < 1:
        return [], [], None

    given_balloon, not_given_balloon = [], []
    last_solved_submission = submissions[0]
    for sub in submissions:
        if in_contest(sub, contest):
            if sub.pk in balloon_subs:
                given_balloon.append(BalloonView(
                                    sub, timestamp=balloon_subs[sub.pk]))
            else:
                not_given_balloon.append(BalloonView(
                                    sub, timestamp=sub.date_uploaded))
        if sub.date_uploaded > last_solved_submission.date_uploaded:
            last_solved_submission = sub

    return given_balloon, not_given_balloon, last_solved_submission

def balloon_home(request, contest_pk=None):
    form = None
    contest = get_most_plausible_contest(contest_pk)
    if not contest:
        return HttpResponse("<h1>There are no contests in the database </h1>")

    if request.method == 'POST':
        form = BalloonSubmissionForm(request.POST)

        if form.is_valid():
            form.save()

    given_balloon, not_given_balloon, last_solved_submission \
            = _get_table_lists(contest)

    if last_solved_submission:
        last_solved_submission = last_solved_submission.pk

    context = {
               'contest'                : contest,
               'contests'               : Contest.objects.all(),
               'given_balloon'          : given_balloon,
               'not_given_balloon'      : not_given_balloon,
               'last_solved_submission' : last_solved_submission,
               }

    return render(request,
                  'balloon_home.html',
                  context,
                  )

admin.site.register(balloon_view, judge_view_admin)

# EOF
