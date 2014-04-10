from __future__ import absolute_import
from execution.models import CompilerProfile, TestCase
from teamsubmission.models import Submission 
from djcelery import celery
from subprocess import call
from openshift.messaging import celery_app as app
import os
import ipdb


WORK_ROOT   = "/idiopen/work/"
FILENAME    = "sauce.in"
FILENAME_SUB = "{FILENAME}"
BASENAME_SUB = "{BASENAME}"

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

def evaluate(submission, compiler, test_cases, limtis):
    os.mkdir(dir_path)
    
    retval, stdout, stderr = compile(submission, compiler)
    
    if retval:
        return 2
        
        

    os.rmdir(dir_path) 


def compile(submission, compiler):
    dir_path = WORK_ROOT + submission.id
    command = 'cd ' + dir_path + ' && ' compiler.compiler_cmd
    command = re.sub(FILENAME_SUB, submission.filename, command)
    command = re.sub(BASENAME_SUB, submission.basename, command) 
    return _run_shell(limits.time, command, False)
    
def execute(submission, compiler, test_cases, limits):
    dir_path = WORK_ROOT + submission.id
    command = 'cd ' + dir_path + ' && ' + compiler.run_cmd
    command = re.sub(BASENAME_SUB, submission.basename)
    command += test_cases.
    return _run_safe_shell(100, command, False)

@app.task
def install_compilers(compilers):
    retval, stdout, stderr = _run_shell(["sudo apt-get update"])
    for compiler in compilers:
        retval, stdout, stderr = _run_shell(["sudo apt-get install " + compiler.package_name])
        if retval:
            raise Exception(stderr)
    ipdb.set_trace()
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

def _run_safe_shell(real_time_limit, command, use_thread = False):
    command = use_run_user(command)
    return _run_shell(real_time_limit, command, use_thread)

def _run_shell(real_time_limit, command, use_thread = False):
    ipdb.set_trace()
    runboy = Runner(command)
    if use_thread:
        start_time = time.time()
        runboy.start()
        while runboy.isAlive():
            tim = time.time() - start_time
            if tim > real_time_limit:
                return 137, 'usertime: %s\nreturn value: 137\n' % tim, ''
    else:
        runboy.run()
    return runboy.retval, runboy.out_stdout, runboy.out_stderr        
     
