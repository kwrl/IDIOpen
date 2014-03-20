from django import forms
from models import Team, Invite, Link
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

class _RadioSelect(forms.RadioSelect):
    def render(self, name, value, attrs=None, choices = ()):
        """ http://tothinkornottothink.com/post/10815277049/django-forms-i-custom-fields-and-widgets-in-detail """
        return super(_RadioSelect, self).render(name, value, attrs, choices);

    def format_output(self, rendered_widgets):
        """
        Given a list of rendered widgets (as strings), returns a Unicode string
        representing the HTML for the whole lot.

        This hook allows you to format the HTML design of the widgets, if
        needed.
        """
        rendered_widgets.insert(0, "<label for=\"id_address_field_0\">Street:</label>");
        rendered_widgets.insert(0, "<label for=\"id_address_field_0\">Street:</label>");
        rendered_widgets.insert(0, "<label for=\"id_address_field_0\">Street:</label>");
        return u''.join(rendered_widgets)

class Team_Form(forms.ModelForm):

    member_one = forms.EmailField(required=False, widget=forms.TextInput(attrs= {'placeholder':'Insert email for team member 1'}));
    member_two = forms.EmailField(required=False, widget=forms.TextInput(attrs= {'placeholder':'Insert email for team member 2'}));
        
    
    def disable_fields(self):
        '''
        If the registration deadline has passed, then disable all fields
        '''
        for _, field in self.fields.items():
            field.widget.attrs['readonly'] = True;
    
    class Meta:
        model = Team      
        widgets = {
                'name' : forms.TextInput(attrs={'placeholder' : 'Insert team name here'}),
                'onsite' : _RadioSelect(choices=ON_OR_OFF, 
                                             attrs ={'onclick' : 'check_radio_button();',
                                                     'id':'id_onsite',}),
                'offsite' : forms.TextInput(attrs={'placeholder' : 'E.g UiO, Aarhus etc '}),
        } 
        fields = ['name', 'onsite', 'offsite']
    
    def clean(self):
        cleaned_data = super(Team_Form, self).clean()
        onsite = cleaned_data.get('onsite')
        offsite = cleaned_data.get('offsite')
        if onsite:
            cleaned_data['offsite'] = ''
            #raise forms.ValidationError("Offsite is required")            
        return cleaned_data
 
 
    #===========================================================================
    # The clean method for the Team Model, didn't work for register team, only
    # for edit team, so I strip whitespace manually here for name and offsite.
    #===========================================================================
    
    def clean_name(self):        
        name = self.cleaned_data.get('name')       
        if not name or name.isspace():
            self._errors['name'] = self.error_class(["Team name is required"])        
        else:
            return self.cleaned_data['name'].strip()   
            
    def clean_offsite(self):
        offsite = self.cleaned_data.get('offsite')
        
        if not offsite or offsite.isspace():
            self._errors['offsite'] = self.error_class(["Offsite is required"])    
        else:
            return self.cleaned_data['offsite'].strip()
 
 
'''
class Team_Form(Team_Base):
=======

    #===========================================================================
    # If onsite is false and offsite is empty, raise ValidationError
    #===========================================================================
    def clean_offsite(self):
        cleaned_data = self.cleaned_data
        onsite = self.cleaned_data['onsite']
        offsite = self.cleaned_data['offsite']
        if not onsite: # if onsite is false
            if not offsite or offsite.isspace(): # if offsite is empty or only contain spaces
                raise forms.ValidationError("You need to fill out your offsite location")
        return offsite
        
    #====================================================================
    # If name only contains white-spaces, raise ValidationError 
    #====================================================================
    def clean_name(self):   
        name = self.cleaned_data['name']
        if name.isspace():
            raise forms.ValidationError('You need a team name')
        return name
 '''           
class Team_Edit(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Team_Edit, self).__init__(*args, **kwargs)
        self.fields['leader'].queryset = self.instance.members.all()
    
    def clean(self):
        cleaned_data = super(Team_Edit, self).clean()
        onsite = cleaned_data.get('onsite')
        offsite = cleaned_data.get('offsite')
        name = cleaned_data.get('name')
        if onsite:
            cleaned_data['offsite'] = ''
        elif not offsite or offsite.isspace():
            self._errors['offsite'] = self.error_class(["Offsite is required"])
            del cleaned_data['offsite']
            #raise forms.ValidationError("Offsite is required")
        if not name or name.isspace():
            self._errors['name'] = self.error_class(["Name is required"])
        
        return cleaned_data
    
    class Meta:
        model = Team 
        widgets = {
                'name' : forms.TextInput(attrs={'placeholder' : 'Insert team name here'} ),
                'onsite' : _RadioSelect(choices=ON_OR_OFF, 
                                             attrs ={'onclick' : 'check_radio_button();',
                                                     'id':'id_onsite',}),
                'offsite' : forms.TextInput(attrs={'placeholder' : 'E.g UiO, Aarhus etc '}),
        } 
        fields = ['name', 'onsite', 'offsite','leader']
    
class CustomSelectMultiple(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return "%s:" %(obj.email)
    

class Team_Add_Members(forms.ModelForm):
    class Meta:
        model = Invite
        fields = ['email']
                
class LinkForm(forms.ModelForm):

    def __init__(self, *args, **kargs):
        super(LinkForm, self).__init__(*args, **kargs)
        self.fields["text"].required = False
        self.fields["url"].required = False 

    

    def clean(self):
        if self.cleaned_data['separator']:
            #import ipdb
            #ipdb.set_trace()
            self.cleaned_data['text'] = u"--------"
            self.cleaned_data['url'] = u"--------"
            #ipdb.set_trace()
            return self.cleaned_data
        elif self.cleaned_data['text'] == None or len(self.cleaned_data['text']) <= 0:
            raise forms.ValidationError("Non-separator links need a text and url field.")
        elif self.cleaned_data['url'] == None or len(self.cleaned_data['url']) <= 0:
            raise forms.ValidationError("Non-separator links need a text and url field.")
        else:
            return self.cleaned_data

    class Meta:
        model   = Link
        fields  = ("url","text","contestUrl","separator")









