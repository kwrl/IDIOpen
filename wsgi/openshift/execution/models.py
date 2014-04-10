from django.db import models    
from contest.models import Contest
from django.conf import settings 

import os

""" Located in media folder (prefix ../media)
"""
PROBLEM_ROOT_DIR = 'problems'

class FileExtension(models.Model):
    extension = models.CharField(max_length=4)
        
    def __unicode__(self):
        return self.extension
    
class CompilerProfile(models.Model):
    name = models.CharField(max_length=100)
    extensions = models.ManyToManyField(FileExtension)
    compiler_name_cmd = models.CharField(max_length=10, blank=True, null=True)

    compiler_flags = models.CharField(max_length=100, blank=True, null=True)

    run_cmd = models.CharField(max_length=10)

    run_flags = models.CharField(max_length=100, blank=True, null=True)
    # How do we handle output filename?

    package_name = models.CharField(max_length=30)
    
    def __unicode__(self):
        return self.name

def get_upload_path(instance, filename):
    """ Dynamically decide where to upload the case,
        based on the foreign key in instance, which is required to be 
        a testcase.
    """
    # path.join appends a trailing / in between each argument
    return os.path.join("%s" % PROBLEM_ROOT_DIR,
                        "%s/case" % (instance.problem),
                        filename);


def get_upload_path2(instance, filename):
    """ Dynamically decide where to upload the case,
        based on the foreign key in instance, which is required to be 
        a testcase.
    """
    # path.join appends a trailing / in between each argument
    return os.path.join("%s" % PROBLEM_ROOT_DIR,
                        filename);

#Author: Tino, Typo
class Problem(models.Model):  
    title = models.CharField(max_length=200, unique = True)
    description = models.TextField()
    textFile = models.FileField(upload_to=get_upload_path2,
                       verbose_name="Text file (file)", blank = True)
    date_uploaded = models.DateTimeField(auto_now = True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL, null = True)
    contest = models.ForeignKey(Contest)
       
    def __unicode__(self):
        return "%s" % (self.title)

class TestCase(models.Model):
    """ We're assuming error cases are defined elsewhere...
        As a python test
    """
    inputFile = models.FileField(upload_to=get_upload_path,
                       verbose_name="Input data (file)")
    outputFile = models.FileField(upload_to=get_upload_path,
                       verbose_name="Output data (file)")
    # inputFile = models.FileField(upload_to=get_upload_path)
    short_description = models.CharField(max_length=40,
                               verbose_name="Description",
                               help_text="Short description of the testcase")
    inputDescription = models.TextField(null=True, blank = True,
                            verbose_name="Description of the" \
                                         " input:")
    outputDescription = models.TextField(null=True, blank = True,
                            verbose_name="Description of the" \
                                         " output:")

    author = models.ForeignKey(settings.AUTH_USER_MODEL, null = True, blank = True, editable = False)
    problem = models.ForeignKey(Problem)

    def __unicode__(self):
        return "%s" % (self.short_description)

# EOF
