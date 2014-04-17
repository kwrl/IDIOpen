from .models import Message 

'''
Created on Apr 16, 2014

@author: tino, typo
'''
from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model=Message
        widgets = {
                'subject' : forms.TextInput(attrs ={'placeholder': 'Title'}),
                'body' : forms.Textarea(attrs ={'placeholder': 'Insert question here'}),
        }       
        
        fields = ['subject', 'body']
        
        