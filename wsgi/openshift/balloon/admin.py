from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.shortcuts import render
from django.conf.urls import url, patterns

from contest.models import Contest, Team
from execution.models import Problem
from teamsubmission.models import Submission

from .models import BalloonStatus
        
from django import forms
from django.forms import ModelForm

class BalloonSubmissionForm(forms.Form):
    submission = forms.ModelChoiceField(queryset=Submission.objects.get_queryset())
    
    class Meta:
        fields = ['problem', 'submission', 'team']
        model = Submission
        
class MyModelAdmin(admin.ModelAdmin):
    # FIXME
    """ Temporary solution to get a view connected iSubmissionn admin site
    """
    view_on_site = True
   
    def get_urls(self):
        urls = super(MyModelAdmin, self).get_urls()
        urls = [urls[0], ]
        my_urls = patterns('',
           url(r'^$', admin.site.admin_view(balloon_home)),
        )

        return my_urls + urls
    
def _get_table_lists():
    balloons = BalloonStatus.objects.all()
    balloon_sub_dict = dict([ball.submission for ball in balloons])
    contest = Contest.objects.get()
    corrrect_submissions = Submission.objects.filter(solved_problem = 'True')
    
    given_balloon, not_given_balloon = [], []
        
    for sub in corrrect_submissions:
        if sub in balloon_sub_dict:
            given_balloon.append(sub)
        else:
            not_given_balloon.append(sub)
            
    return given_balloon, not_given_balloon

def balloon_home(request):
    given_balloon, not_given_balloon = _get_table_lists()
    
    if request.method == 'POST':
        import ipdb; ipdb.set_trace()
        pass
        
    else:
        pass
       
    context = {
               'given_balloon': given_balloon,
               'not_given_balloon': not_given_balloon,
               'test' : BalloonSubmissionForm(),
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

admin.site.register(balloon_view, MyModelAdmin)

# EOF