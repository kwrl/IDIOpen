from django.db import models    
from contest.models import Contest
from django.conf import settings 

import os

""" Located in media folder (prefix ../media)
"""
PROBLEM_ROOT_DIR = 'problems'

class FileExtension(models.Model):
    extension = models.CharField(max_length=4)

class CompilerProfile(models.Model):
    extensions = models.ManyToManyField(FileExtension)
    compiler_name_cmd = models.CharField(max_length=10)

    flags = models.CharField(max_length=100)
    # How do we handle output filename?

    package_name = models.CharField(max_length=30)

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
                        "problemDesc",
                        filename);

#Author: Tino, Typo
class Problem(models.Model):  
    title = models.CharField(max_length=200)
    description = models.TextField()
    textFile = models.FileField(upload_to=get_upload_path2,
                       verbose_name="Text file (file)", blank = True)
    date_uploaded = models.DateTimeField(auto_now = True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL, null = True)
    contest = models.ForeignKey(Contest)
       
    def __unicode__(self):
        return "%s" % (self.description)

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

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null = True)
    problem = models.ForeignKey(Problem)

    def __unicode__(self):
        return "%s" % (self.short_description)

# EOF
