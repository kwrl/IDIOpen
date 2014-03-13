from django import forms
from models import Team
from django.forms.widgets import CheckboxSelectMultiple
from django.forms.models import ModelMultipleChoiceField
from userregistration.models import CustomUser

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
    
class CustomSelectMultiple(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return "%s:" %(obj.email)
    
class Team_Delete_Members(forms.ModelForm):
    #  members = ModelMultipleChoiceField(widget=CheckboxSelectMultiple(), required=True)
  
    def __init__(self,*args,**kwargs):
        super(Team_Delete_Members, self).__init__(*args,**kwargs)
        #qs = Team.objects.get(pk = self.instance.pk)
        self.fields['members'] = ModelMultipleChoiceField(
            # TODO exlude leader from qs
            queryset= CustomUser.objects.filter(members__in=Team.objects.filter(pk = self.instance.pk)), 
                                       widget=CheckboxSelectMultiple())
    class Meta:
        model = Team
        fields = ['members']
    #    widgets = {'members':CheckboxSelectMultiple(),}
