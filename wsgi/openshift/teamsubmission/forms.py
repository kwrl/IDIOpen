from django import forms
from openshift.teamsubmission.models import Submission
from django.template.defaultfilters import filesizeformat
from django.core.exceptions import ValidationError
from openshift.execution.models import FileExtension, CompilerProfile
from openshift.node_manage.tasks import evaluate_task
# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160
MAX_UPLOAD_SIZE = "5242880" # 5 MB

# Maybe not the best way
def get_file_extensions():
    return FileExtension.objects.all()
 
class SubmissionForm(forms.ModelForm):
    
    class Meta:
        model = Submission  
        fields = ['submission']
        
    def clean(self):
        submission = self.cleaned_data.get('submission')
        if not submission:
            self._errors['submission'] = self.error_class([("Please upload a file before submitting")])
            raise ValidationError('')
        # The file extension for the given submission
        content_type = submission.name.split('.')[-1]
        FILE_EXT = get_file_extensions()
        # Check if submission has an allowed file extension
        if content_type in [str(x) for x in FILE_EXT]:
            if submission._size > MAX_UPLOAD_SIZE:
                self._errors['submission'] = self.error_class([('Please keep filesize under %s. Current filesize %s') % (filesizeformat(MAX_UPLOAD_SIZE), filesizeformat(submission._size))])
        else:
            self._errors['submission'] = self.error_class([('File type is not supported')])
        return self.cleaned_data
    
    def save(self):
        new_sub = Submission()
        new_sub.submission = self.cleaned_data.get('submission')
        new_sub.problem = self.instance.problem
        new_sub.validate = False
        new_sub.team = self.instance.team
        new_sub.save()
        #evaluate_task(new_sub.pk, compiler_id, test_case_ids, limit_id)

# EOF