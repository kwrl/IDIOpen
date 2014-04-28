
'''
Created on Apr 16, 2014

@author: tino, typo
'''
from .models import Question 
from openshift.helpFunctions import views as helpView
from django import forms

class QuestionForm(forms.ModelForm):
    '''
    Form for submitting questions to the clarification system.
    Does little of note other than stripping subject and body.
    '''
    class Meta:
        model=Question
        widgets = {
                'subject' : forms.TextInput(attrs ={'placeholder': 'Title'}),
                'body' : forms.Textarea(attrs ={'placeholder': 'Insert question here'}),
        }       
        
        fields = ['subject', 'body']
        
    def save(self,data):
        subject             = self.cleaned_data['subject'].strip()
        body                = self.cleaned_data['body'].strip()
        new_message         = Question()
        new_message.body    = body
        new_message.subject = subject
        new_message.contest = data['contest']
        new_message.sender  = data['sender']
        new_message.save()
