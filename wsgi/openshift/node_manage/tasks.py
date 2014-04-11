from __future__ import absolute_import
from openshift.execution.models import CompilerProfile, TestCase
from openshift.teamsubmission.models import Submission 
from subprocess import call
from openshift.messaging import celery_app as app

import re
import os
#import ipdb
import threading
import time
import popen2

WORK_ROOT   = "/idiopen/work/"
FILENAME    = "sauce.in"
FILENAME_SUB = "{FILENAME}"
BASENAME_SUB = "{BASENAME}"

RUN_USER = "algrun"

"""
Evaluation return values:
0   -   Correct
1   -   Wrong answer
2   -   Compile time error
3   -   Timed out or out of memory
4   -   Runtime error
5   -  Correct
1   -   Wrong answer
"""



@app.task
def add(x, y):
    return x + y

@app.task
def evaluate_task(submission_id, compiler_id, test_case_ids, limit_id):
    sub     = Submission.objects.get(pk=submission_id)
    comp    = CompilerProfile.objects.get(pk=compiler_id)
    test_cases = TestCase.objects.filter(pk__in=test_case_ids)
    #limit   = get some freaking limits, br0  
    evaluate(sub,comp,test_cases,None)
    return (submission_id, compiler_id, test_case_ids, limit_id)

def evaluate(submission, compiler, test_cases, limits):
    dir_path = WORK_ROOT + str(submission.id) + str(os.getpid())
    os.mkdir(dir_path)
    
    retval, stdout, stderr = compile(submission, compiler)
    results = execute(submission, compiler, test_cases, limits)
    if retval:
        return 2
        
        

    os.rmdir(dir_path) 


def compile(submission, compiler):
    dir_path = WORK_ROOT + str(submission.id) + str(os.getpid())
    command = 'cd ' + dir_path + ' && '+ compiler.compile
    command = re.sub(FILENAME_SUB, submission.submission, command)
    command = re.sub(BASENAME_SUB, submission.submission.filename.split(".")[0], command) 
    return _run_shell(command)
    
def execute(submission, compiler, test_cases, limits):
    dir_path = WORK_ROOT + str(submission.id) + str(os.getpid())
    command = 'cd ' + dir_path + ' && ' + compiler.run
    command = re.sub(BASENAME_SUB, submission.basename)
    results = []
    for test in test_cases:
        retval, stdout, stderr = _run_safe_shell(command + ' ' + test.inputfile + ' | tee output.txt')
        diff = _run_shell('diff ' + dir_path + '/output.txt ' + test.inputfile)
        results.append([retval, stdout, stderr, diff])
    
    #command += test_cases.
    return results

def run_test(submission, comp):
    dir_path = WORK_ROOT + submission.id
    command = 'cd ' + dir_path + ' && ' + comp.run_cmd
    re.sub(BASENAME_SUB, submission.submission.split(".")[0])

@app.task
def install_compilers(compilers):
    retval, stdout, stderr = _run_shell(["sudo apt-get update"])
    for compiler in compilers:
        retval, stdout, stderr = _run_shell("sudo apt-get install " + compiler.package_name)
        if retval:
            raise Exception(stderr)
    #ipdb.set_trace()
    return stdout
       

class Runner(threading.Thread):
    def __init__(self, command):
        self.command = command
        self.retval = 255
        self.out_stdout = ''
        self.out_stderr = ''

    def run(self):
        proc = popen2.Popen3(self.command, True)
        pi, po, pe = proc.tochild, proc.fromchild, proc.childerr
        pi.close()
        self.out_stdout = po.read()
        self.out_stderr = pe.read()
        po.close()
        pe.close()
        while (proc.poll() == -1):
            time.sleep(0.001)
        self.retval = proc.poll()

class RawTestCase:
    def __init__(self, test_case):
        test_case.inputFile.open("rb")
        test_case.outputFile.open("rb")
        self.input_content = test_case.inputFile.read()
        self.output_content= test_case.outputFile.read()
    
def _run_safe_shell(command):
    command = use_run_user(command)
    return _run_shell(command)

def use_run_user(command):
    return 'nice sudo su ' + RUN_USER + ' -c "' + command + '"'

def _run_shell(command):
    #ipdb.set_trace()
    runboy = Runner(command)
    runboy.run()
    
    return runboy.retval, runboy.out_stdout, runboy.out_stderr        
    
@app.task
def uname():
    retval, stdout, stderr = _run_shell("hostname")
    return stdout



 
