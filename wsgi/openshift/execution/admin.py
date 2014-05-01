from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import AdminTextInputWidget
from .models import TestCase, Problem, CompilerProfile, FileExtension, Resource


class TestCaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'problem', 'compileProfile', 'author' )
    def name(self, obj):
        return obj # uses the toString method
    # search_fields = ('name', '',)
    ordering = ('inputFile','inputDescription', 
                'outputFile', 'outputDescription')
    
    fieldsets = (
        (None, {
            'fields': ('inputFile', 'outputFile', 'short_description', 'inputDescription',
                       'outputDescription', 'problem')
        }),
        ('Custom validator', {
            'fields': ('compileProfile', 'validator'),
            'description': 'If your output is floating point or requires a custom validator' \
            ' you can specify the custom validator here. The file will get compiled with the compiler profile you specify.',
        }),
    )


class ProblemAdmin(admin.ModelAdmin):
    search_fields = ('title', 'author',)
    list_display = ('title', 'author', 'contest') 
    list_filter = ('contest',)
    fields = ('title', 'description', 'textFile', 'contest')
    # Set author, to the user/admin who created the article
    def save_model(self, request, obj, form, change):
        # Only update author if author = None
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save() 
    class Media:
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/openshift/js/tinymce_setup.js',
        ]
        
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'cProfile', 'problem', 'max_compile_time')
    list_filter = ('cProfile', )
    def name(self, obj):
        return obj
    fieldsets = (
        (None, {
            'fields': ('cProfile', 'problem')
        }),
        ('Resource Limits', {
            'fields': ('max_compile_time', 'max_program_timeout',
                       'max_memory', 'max_processes', 'max_filesize'),
            'description': 'Here you set the limits for a problem and for a compiler profile. The system uses <strong>rlimit</strong>' \
            ' to enforce these limits. <br> Java does <strong>not</strong> work very well here and you might have to set the limits directly on the compiler ' \
            ' profile for Java and the limits here should be set to <strong>-1</strong>. This means unlimited'
        }),
    
    )
    
    
class CompilerProfileForm(forms.ModelForm):
    class Meta:
        model = CompilerProfile
        widgets = {
                  'compile' : AdminTextInputWidget(attrs={'placeholder' : 'gcc -w --std=c99 -O2 -o {BASENAME} {FILENAME} -lm'}),
                  'run' : AdminTextInputWidget(attrs={'placeholder' : './{BASENAME}'}),
                  'package_name' : AdminTextInputWidget(attrs={'placeholder': 'gcc'})
        }
    
class CompilerProfileAdmin(admin.ModelAdmin):
    form = CompilerProfileForm
    

class FileExtensionForm(forms.ModelForm):
    class Meta:
        model = FileExtension
        widgets = {
                  'extension' : AdminTextInputWidget(attrs={'placeholder' : '*.{File extension}'})
        }

class FileExtensionAdmin(admin.ModelAdmin):
    form = FileExtensionForm
     
        
admin.site.register(Problem, ProblemAdmin)
admin.site.register(FileExtension, FileExtensionAdmin)
admin.site.register(CompilerProfile, CompilerProfileAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(TestCase, TestCaseAdmin)
