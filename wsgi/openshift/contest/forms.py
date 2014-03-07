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
    email_one = forms.EmailField(required=False);
    email_two = forms.EmailField(required=False);
      
    class Meta:
        model = Team
        fields = ['name', 'onsite', 'offsite']