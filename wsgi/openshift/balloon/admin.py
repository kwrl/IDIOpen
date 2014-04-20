from django import forms
from django.contrib import admin
from django.db import models
from django.shortcuts import render
from django.conf.urls import url, patterns

from openshift.contest.models import Contest, Team
from openshift.execution.models import Problem
from openshift.teamsubmission.models import Submission
from .models import BalloonStatus
from .forms import BalloonSubmissionForm

class judge_view_admin(admin.ModelAdmin):
    # FIXME
    """ Temporary solution to get a view connected iSubmissionn admin site
    """
    view_on_site = True
   
    def get_urls(self):
        urls = super(judge_view_admin, self).get_urls()
        urls = [urls[0], ]
        my_urls = patterns('',
           url(r'^$', admin.site.admin_view(balloon_home)),
        )
        return my_urls + urls
    
class BalloonView(object):
    def __init__(self, submission, timestamp=None):
        self.submission = submission
        self.timestamp = timestamp
    
def _get_table_lists():
    balloons = BalloonStatus.objects.all()
    balloon_subs = dict([(ball.submission.pk, ball.timestamp) for ball in balloons])
    corrrect_submissions = Submission.objects.filter(team__onsite = 'True').filter(solved_problem = 'True')
    
    given_balloon, not_given_balloon = [], []
        
    for sub in corrrect_submissions:
        if sub.pk in balloon_subs:
            given_balloon.append(BalloonView(
                                sub, timestamp=balloon_subs[sub.pk]))
        else:
            not_given_balloon.append(BalloonView(
                                sub, timestamp=sub.date_uploaded))
    return given_balloon, not_given_balloon

def balloon_home(request):
   
    form = None
    if request.method == 'POST':
        form = BalloonSubmissionForm(request.POST);
        
        if form.is_valid():
            form.save()
        pass
        
    else:
        pass
       
    given_balloon, not_given_balloon = _get_table_lists()
    context = {
               'given_balloon': given_balloon,
               'not_given_balloon': not_given_balloon,
               }

    return render(request,
                  'balloon_home.html',
                  context,
                  )

class string_with_title(str):
    def __new__(cls, value, title):
        instance = str.__new__(cls, value)
        instance._title = title
        return instance

    def title(self):
        return self._title

    __copy__ = lambda self: self
    __deepcopy__ = lambda self, memodict: self


class balloon_view(models.Model):
    class Meta:
        app_label = string_with_title("Balloon_table", "Balloon_table")

        managed = False # prevent from entering the DB
        verbose_name = "Click here to view balloon table"
        verbose_name_plural = "Click here to view balloon table"

admin.site.register(balloon_view, judge_view_admin)

# EOF