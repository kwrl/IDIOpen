from django import forms
from openshift.teamsubmission.models import Submission
from django.template.defaultfilters import filesizeformat
from django.core.exceptions import ValidationError
from openshift.execution.models import FileExtension, CompilerProfile, Resource
from openshift.node_manage.tasks import evaluate_task
from openshift.messaging import celery_app
from django.forms.widgets import FileInput, ClearableFileInput
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape, format_html
import os
# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160
MAX_UPLOAD_SIZE = "5242880" # 5 MB

# Maybe not the best way, could get file extensions for each compiler profile connected to a specific problem
def get_file_extensions():
    return FileExtension.objects.all()

def get_max_file_size(problem, cProfile):
    resource = Resource.objects.filter(problem=problem).filter(cProfile=cProfile)
    if resource:
        return resource[0].max_filesize
    else:
        # No resource found so return 0
        return 0
    
class FileInputInitial(ClearableFileInput):
    
    initial_text = 'Last uploaded'
    input_text = 'Change'
    clear_checkbox_label = 'Clear'

    template_with_initial = '%(initial_text)s: %(initial)s <br />%(input_text)s: %(input)s'

    url_markup_template = '{0}'

    def render(self, name, value, attrs=None):
        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
        }
        template = '%(input)s'
        substitutions['input'] = super(ClearableFileInput, self).render(name, value, attrs)

        if value and hasattr(value, "url"):
            template = self.template_with_initial
            #substitutions['initial'] = format_html(self.url_markup_template,
            #                                       force_text(os.path.split(os.path.abspath(value.path))[1]))
            substitutions['initial'] = force_text(os.path.split(os.path.abspath(value.path))[1])
        return mark_safe(template % substitutions)

class SubmissionForm(forms.ModelForm):
    #compilerProfile = forms.ModelChoiceField(CompilerProfile.objects.all())
    
    class Meta:
        model = Submission  
        fields = ['submission', 'compileProfile']
        widgets = {'submission' : FileInputInitial(),}
        
    
        
    def clean(self):
        submission = self.cleaned_data.get('submission')
        cProfile = self.cleaned_data.get('compileProfile')
        
        if not submission:
            self._errors['submission'] = self.error_class([("Please upload a file before submitting")])
            raise ValidationError('')
        # The file extension for the given submission
        content_type = submission.name.split('.')[-1]
        FILE_EXT = get_file_extensions()
        MAX_FILESIZE = get_max_file_size(self.instance.problem, cProfile) * 1024 # Multiply with 1024 to get it in KB instead of Bytes
        # MAX_FILESIZE = 0 when no resource is found
        if (MAX_FILESIZE == 0):
            self._errors['compileProfile'] = self.error_class([('No resource set for the compiler profile selected')])
            return self.cleaned_data
        # Check if submission has an allowed file extension
        if content_type in [str(x) for x in FILE_EXT]:
            if submission._size > MAX_FILESIZE:
                self._errors['submission'] = self.error_class([('Please keep filesize under %s. Current filesize %s') % (filesizeformat(MAX_FILESIZE), filesizeformat(submission._size))])
        else:
            self._errors['submission'] = self.error_class([('File type is not supported')])
        return self.cleaned_data
    
    def save(self):
        new_sub = Submission()
        new_sub.submission = self.cleaned_data.get('submission')
        new_sub.compileProfile = self.cleaned_data.get('compileProfile')
        new_sub.problem = self.instance.problem
        new_sub.validate = False
        new_sub.team = self.instance.team
        new_sub.status = new_sub.QUEUED
        new_sub.save()
       #print 'running task'
        evaluate_task.delay(new_sub.pk)

# End of life
