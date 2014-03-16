from django import forms
from models import Team, Invite
from django.forms.widgets import CheckboxSelectMultiple, Widget
from django.forms.models import ModelMultipleChoiceField
from userregistration.models import CustomUser

'''
Created on Feb 12, 2014

@author: tino, haakon 
'''
'''
TODO: add support for leader. We need the log in to do that.
support for leader is added. This is done in the view
'''


ON_OR_OFF = ((True, 'Yes'), (False, 'No')) 

class Team_Edit(forms.ModelForm):
    class Meta:
        model = Team      
        widgets = {
                'name' : forms.TextInput(attrs={'placeholder' : 'Insert team name here'}),
                'onsite' : forms.RadioSelect(choices=ON_OR_OFF, 
                                             attrs ={'onclick' : 'check_radio_button();'}),
        } 
        fields = ['name', 'onsite', 'offsite']

class Team_Form(Team_Edit):
    member_one = forms.EmailField(required=False, widget=forms.TextInput(attrs= {'placeholder':'Insert email for team member 1'}));
    member_two = forms.EmailField(required=False, widget=forms.TextInput(attrs= {'placeholder':'Insert email for team member 2'}));

    def disable_fields(self):
        for _, field in self.fields.items():
            field.widget.attrs['readonly'] = True;
    
class CustomSelectMultiple(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return "%s:" %(obj.email)
    
class Team_Delete_Members(forms.ModelForm):
    #  members = ModelMultipleChoiceField(widget=CheckboxSelectMultiple(), required=True)
  
    def __init__(self,*args,**kwargs):
        super(Team_Delete_Members, self).__init__(*args,**kwargs)
        #qs = Team.objects.get(pk = self.instance.pk)
        self.fields['members'] = ModelMultipleChoiceField(
            queryset= CustomUser.objects.filter(members__in=Team.objects.filter(pk = self.instance.pk)).exclude(pk=self.instance.leader.pk), 
                                       widget=CheckboxSelectMultiple(), required=False)
    class Meta:
        model = Team
        fields = ['members']
    #    widgets = {'members':CheckboxSelectMultiple(),}

class Team_Add_Members(forms.ModelForm):
    class Meta:
        model = Invite
        fields = ['email']
                
