from django.db import models
from django.conf import settings

import os

""" Located in media folder (prefix ../media)
"""
PROBLEM_ROOT_DIR = 'problems'

class FileExtension(models.Model):
    extension = models.CharField(max_length=4, help_text = 'e.g java, c or cpp. Write the extension name without dot in front. ')

    def __unicode__(self):
        return self.extension

class CompilerProfile(models.Model):
    name = models.CharField(max_length=100)
    extensions = models.ManyToManyField('FileExtension')
    
    compile = models.CharField(max_length=100, blank=True, null=True,
                               help_text=
                               'The command to compile, include {BASENAME} for file without extension' + 
                               ' {FILENAME} for file with extension, include all flags required' + 
                               '<br>Example: gcc -w --std=c99 -O2 -o {BASENAME} {FILENAME} -lm')


    run = models.CharField(max_length=100,
                           help_text=
                           'The command to run the program, include {BASENAME} for file without extension' + 
                           ' {FILENAME} for file with extension, include all flags required' + 
                           '<br>Example: java {BASENAME} <br>Example2: ./{BASENAME')

    # The name of the package that is required in order to install the compiler. (Via apt-get)
    package_name = models.CharField(max_length=30, 
                                    help_text='The package required to run and compile, eg. openjdk-7-jdk')

    def __unicode__(self):
        return self.name


def get_resource(submission, compiler):
    try: 
        prob = Problem.objects.get(pk=submission.problem.pk)
        res = Resource.objects.filter(problem=prob).filter(cProfile=compiler)[0]
    except Exception:
        return None
    return res

def get_upload_path(instance, filename):
    """ Dynamically decide where to upload the case,
        based on the foreign key in instance, which is required to be
        a testcase.
    """
    # path.join appends a trailing / in between each argument
    return os.path.join("%s" % PROBLEM_ROOT_DIR,
                        "%s/case" % (instance.problem),
                        filename)

def get_upload_path2(instance, filename):
    """ Dynamically decide where to upload the case,
        based on the foreign key in instance, which is required to be
        a testcase.
    """
    # path.join appends a trailing / in between each argument
    return os.path.join("%s" % PROBLEM_ROOT_DIR,
                        filename)

#Author: Tino, typo
class Problem(models.Model):
    title       = models.CharField(max_length=200, unique = True)
    description = models.TextField()
    textFile    = models.FileField(upload_to=get_upload_path2,
                       verbose_name="Text file (file)", blank = True)
    date_uploaded   = models.DateTimeField(auto_now = True)
    author          = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL, null = True)
    contest         = models.ForeignKey('contest.Contest')
    
    resource        = models.ManyToManyField('execution.CompilerProfile', through='Resource')

    def __unicode__(self):
        return "%s" % (self.title)

#Author: typo
class Resource (models.Model):
    '''
    This models contains all "limitations" on each Profile. 
    E.g. the number maximum memory usage for this profile, if JAVA is used is XXXXX. 
    '''
    cProfile = models.ForeignKey('execution.CompilerProfile', related_name="resource_CompilerProfile")
    problem = models.ForeignKey('execution.Problem', related_name="resource_problem")
    
    #The maximum time a program can use to compile
    max_compile_time = models.IntegerField(max_length = 20, default = 10,
                                           help_text = 'The maximum compile time in <strong>seconds</strong>') #in sec
    
    #How long the program can run before 
    max_program_timeout = models.IntegerField(max_length = 5, default = 2,
                                              help_text = 'The maximum run time in <strong>seconds</strong>')# in sec 
    
    #Maximum memory a program can use for this problem  
    max_memory = models.IntegerField(max_length = 20, default = 1024,
                                     help_text = 'The maximum adress space in <strong>MegaBytes</strong>. For java use -1(unlimited).') # in bytes
    
    #The maximum number of child processes. (avoid fork bombs)
    max_processes = models.IntegerField(max_length = 10, default = 5,
                                        help_text = 'The maximum number of processes. Java needs a minimum of 10.')
     
    #Maximum filesize, 
    max_filesize = models.IntegerField(max_length = 10, default = 50,
                                       help_text = 'The maximum uploaded file size in <strong>KiloBytes</strong>')
        
    '''
    From the old code: 
        
    MAX_COMPILE_TIME = 30.0 # In sec. 
    MAX_PROGRAM_TIMEOUT = 60 # In sec 
    MAX_MEM = 100000 # kilobytes
    MAX_PROC = 5 # maximum number of child processes (avoid fork bombs)
    '''
    
    def __unicode__(self):
        return self.problem.title + ' ' + self.cProfile.name 
    

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

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null = True, blank = True, editable = False)
    problem = models.ForeignKey('execution.Problem')

    compileProfile  = models.ForeignKey(CompilerProfile, null=True, blank=True)
    validator       = models.FileField(upload_to=get_upload_path,null=True, blank=True,
                            verbose_name="Custom validator source")

    def __unicode__(self):
        return "%s" % (self.short_description)


# EOF
