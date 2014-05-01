from django.contrib import admin
from django import forms
from django.db import models
from django.contrib.admin.widgets import AdminTextInputWidget, AdminTextareaWidget, AdminIntegerFieldWidget
from .models import Submission, ExecutionLogEntry

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('date_uploaded', 'text_feedback', 'team', 'problem',
                    'solved_problem', 'submission', 'contest')
    list_filter = ('team', 'team__contest', 'solved_problem')
    search_fields = ('team', 'contest')

class ExecutionLogEntryAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget':AdminTextInputWidget(attrs={'readonly':'readonly'})},
        models.TextField: {'widget':AdminTextareaWidget(attrs={'readonly':'readonly','rows':40})},
        models.IntegerField: {'widget':AdminIntegerFieldWidget(attrs={'readonly':'readonly'})},
        models.ForeignKey: {'widget':forms.Select(attrs={'disabled':'disabled'})}
    }
    list_display = ('submission', 'command', 'retval', 'team', 'contest')
    search_fields = ('submission', 'team')
    list_filter = ('submission__team','submission__team__contest')

    def has_add_permission(self, request):
        return False

admin.site.register(Submission, SubmissionAdmin)
admin.site.register(ExecutionLogEntry,ExecutionLogEntryAdmin)

# EOF
