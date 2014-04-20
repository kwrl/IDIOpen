from django import forms

from .models import BalloonStatus
import datetime

from openshift.execution.models import Problem
from openshift.teamsubmission.models import Submission

class BalloonSubmissionForm(forms.Form):
    pk = forms.IntegerField()
    
    def clean(self):
        try:
            Submission.objects.get(pk=self.cleaned_data.get('pk'))
        except Exception:
            pass
            
        return self.cleaned_data
    
    def save(self):
        submission = Submission.objects.get(pk=self.cleaned_data['pk'])

        if not BalloonStatus.objects.filter(submission=submission).exists():
            new_model = BalloonStatus()
            new_model.submission = Submission.objects.get(pk=self.cleaned_data['pk'])
            new_model.problem = new_model.submission.problem
            new_model.team = new_model.submission.team
            new_model.timestamp = datetime.datetime.now()
            new_model.save()
        else:
            obj = BalloonStatus.objects.get(submission=submission);
            obj.delete()
            

# EOF