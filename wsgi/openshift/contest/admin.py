from django.contrib import admin
from django.core.exceptions import ValidationError;
from django.forms import ModelForm;
from contest.models import Contest, Link, Team

class ContestForm(ModelForm):

    # def clean_start_date(self):
        # At this point, end_date is not cleaned, hence it's troublesome
        #to validate both.

        # start_data = self.cleaned_data['start_date'];
        # end_data_0 = self.data['end_date_0'];
        # end_data_1 = self.data['end_date_1'];

        # if start_date is not None and end_date is not None:
        #     if start_date.__lt__(end_date) == False:
        #         raise ValidationError('You cannot set start date to be after the end date');

    def clean_end_date(self):
        """ Checks to ensure that start_date is before end_date
             Automatically invoked whenever form is submitted.
        """
        start_date = self.cleaned_data['start_date'];
        end_date = self.cleaned_data['end_date'];

        # if start_date is not None and end_date is not None: # implicit from key
        if start_date.__lt__(end_date) == False:
            raise ValidationError('You cannot set end date to be before the start date');

        return end_date;
        
    class Meta:
        model = Contest;

class ContestAdmin(admin.ModelAdmin):
    form = ContestForm;

admin.site.register(Contest, ContestAdmin)
admin.site.register(Link)
admin.site.register(Team)

# EOF
