from django.contrib import admin
from .models import Submission
# Register your models here.

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('date_uploaded', 'text_feedback', 'team', 'problem', 'solved_problem', 'submission')


admin.site.register(Submission, SubmissionAdmin)
