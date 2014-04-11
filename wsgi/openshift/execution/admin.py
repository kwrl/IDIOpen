from django.contrib import admin

from .models import TestCase, Problem, CompilerProfile, FileExtension, Resource


class TestCaseAdmin(admin.ModelAdmin):
    # list_display = ('short_description')
    # search_fields = ('name', '',)
    ordering = ('inputFile','inputDescription', 
                'outputFile', 'outputDescription')

admin.site.register(TestCase, TestCaseAdmin)

class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'contest') 
    fields = ('title', 'description', 'textFile', 'contest')
    # Set author, to the user/admin who created the article
    def save_model(self, request, obj, form, change):
        # Only update author if author = None
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()        
        
admin.site.register(Problem, ProblemAdmin)
admin.site.register(FileExtension)
admin.site.register(CompilerProfile)
admin.site.register(Resource)
