'''
Created on 12. feb. 2014

@author: tinokul
'''
from django import forms

class TeamForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    team_type = forms.CharField()
    
    