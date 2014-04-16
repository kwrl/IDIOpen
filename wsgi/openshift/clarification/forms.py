'''
Created on Apr 16, 2014

@author: tino
'''
from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    
    class Meta:
        