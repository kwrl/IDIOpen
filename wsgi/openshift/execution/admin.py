from django.contrib import admin

from .models import TestCase, Problem

class TestCaseAdmin(admin.ModelAdmin):
    # list_display = ('short_description')
    # search_fields = ('name', '',)
    ordering = ('inputFile','inputDescription', 
                'outputFile', 'outputDescription')

admin.site.register(TestCase, TestCaseAdmin)

class ProblemAdmin(admin.ModelAdmin):
    ordering = ('title', 'description', 'textFile')
    
admin.site.register(Problem, ProblemAdmin)
