from django import forms
from models import Team

'''
Created on Feb 12, 2014

@author: tino, haakon 
'''


'''
TODO: add support ofor leader. We need the log in to do that.
'''
class Team_Form(forms.ModelForm):
    email_one = forms.EmailField();
    email_two = forms.EmailField();
      
    class Meta:
        model = Team
        fields = ['team_name', 'onsite', 'offsite']