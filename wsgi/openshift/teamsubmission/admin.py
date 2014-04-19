from django.contrib import admin
from django import forms

from .models import Submission, ExecutionLogEntry

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('date_uploaded', 'text_feedback', 'team', 'problem',
                    'solved_problem', 'submission')

class ExecutionLogEntryForm(forms.ModelForm):
    class Meta:
        model=ExecutionLogEntry
        
        widgets={   'stdout':forms.Textarea(attrs={'readonly':'readonly','rows':10, 'cols':5}),
                    'stderr':forms.Textarea(attrs={'readonly':'readonly','rows':10, 'cols':5}),
                    'retval':forms.TextInput(attrs={'readonly':'readonly'}),
                    'submission':forms.Select(attrs={'disabled':'disabled'}),
                    'command':forms.TextInput(attrs={'readonly':'readonly'})}

class ExecutionLogEntryAdmin(admin.ModelAdmin):
    form = ExecutionLogEntryForm
    def has_add_permission(self, request):
        return False

admin.site.register(Submission, SubmissionAdmin)
admin.site.register(ExecutionLogEntry,ExecutionLogEntryAdmin)

# EOF
