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
        
    def clean(self):
        cleaned_data = super(Team_Form, self).clean()
        onsite = cleaned_data.get('onsite')
        offsite = cleaned_data.get('offsite')
        if onsite:
            cleaned_data['offsite'] = ''
        elif not offsite or offsite.isspace():
            self._errors['offsite'] = self.error_class(["Offsite is required"])
            del cleaned_data['offsite']
            #raise forms.ValidationError("Offsite is required")
            
        name = cleaned_data['name']
        if name.isspace():
            self._errors['name'] = self.error_class(["Name is required"])
            del cleaned_data['name']
            
        return cleaned_data
    
    
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
        if onsite:
            cleaned_data['offsite'] = ''
        elif not offsite or offsite.isspace():
            self._errors['offsite'] = self.error_class(["Offsite is required"])
            del cleaned_data['offsite']
            #raise forms.ValidationError("Offsite is required")
        name = cleaned_data['name']
        if name.isspace():
            self._errors['name'] = self.error_class(["Name is required"])
            del cleaned_data['name']    
        
        return cleaned_data
    
    class Meta:
        model = Team 
        widgets = {
                'name' : forms.TextInput(attrs={'placeholder' : 'Insert team name here'}),
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
                

