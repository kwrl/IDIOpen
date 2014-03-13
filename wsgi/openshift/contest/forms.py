from django import forms
from models import Team

'''
Created on Feb 12, 2014

@author: tino, haakon 
'''


'''
TODO: add support for leader. We need the log in to do that.
'''
class Team_Edit(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'onsite', 'offsite']

class Team_Form(Team_Edit):
    email_one = forms.EmailField(required=False);
    email_two = forms.EmailField(required=False);
      
    