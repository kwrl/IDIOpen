from django import forms
from models import Team

'''
Created on Feb 12, 2014

@author: tino, haakon 
'''

class Team_Form(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['team_name', 'onsite', 'offsite']
        