from django.contrib import admin
from django import forms
from django.db import models

from .models import Submission, ExecutionLogEntry

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('date_uploaded', 'text_feedback', 'team', 'problem',
                    'solved_problem', 'submission')

class ExecutionLogEntryAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget':forms.TextInput(attrs={'readonly':'readonly','size':'30'})},
        models.TextField: {'widget':forms.Textarea(attrs={'readonly':'readonly','rows':40,'cols':40})},
        models.IntegerField: {'widget':forms.TextInput(attrs={'readonly':'readonly'})},
        models.ForeignKey: {'widget':forms.Select(attrs={'disabled':'disabled'})}
    }

    def has_add_permission(self, request):
        return False

admin.site.register(Submission, SubmissionAdmin)
admin.site.register(ExecutionLogEntry,ExecutionLogEntryAdmin)

# EOF
