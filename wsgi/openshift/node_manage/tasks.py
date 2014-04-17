from __future__ import absolute_import
from openshift.execution.models import CompilerProfile, TestCase, Resource, get_resource
from openshift.teamsubmission.models import Submission 
from subprocess import call
from openshift.messaging import celery_app as app
from subprocess import PIPE, Popen
import re
import os
import threading
import time
import popen2
import pwd
import shlex
import resource


WORK_ROOT   = "/idiopen/work/"
FILENAME    = "sauce.in"
FILENAME_SUB = "{FILENAME}"
BASENAME_SUB = "{BASENAME}"

RUN_USER = "gentlemember"

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

def getUserData():
    pw_record = pwd.getpwnam(RUN_USER)
    user_uid       = pw_record.pw_uid
    user_gid       = pw_record.pw_gid
    return user_uid, user_gid

def demote(user_uid, user_gid):
    def result():
        os.setgid(user_gid)
        os.setuid(user_uid)
    return result

def set_resource(time, memory, procs):
    def result():
        nproc   = resource.getrlimit(resource.RLIMIT_NPROC)
        tcpu    = resource.getrlimit(resource.RLIMIT_CPU)
        mem     = resource.getrlimit(resource.RLIMIT_DATA)

        nproc[0]    = procs
        tcpu[0]     = time
        mem[0]      = memory

        # Set The maximum number of processes the current process may create.
        resource.setrlimit(resource.RLIMIT_NPROC, nprocs)
        # Set The maximum amount of processor time (in seconds) that a process can use.
        resource.setrlimit(resource.RLIMIT_CPU, tcpu)
        # Set The maximum area (in bytes) of address space which may be taken by the process.
        resource.setrlimit(resource.RLIMIT_DATA, mem)

    return result
    #limit.max_program_timeout, limit.max_memory, limit.max_processes

@app.task
def add(x, y):
    return x + y

@app.task
def evaluate_task(submission_id):
    sub     = Submission.objects.get(pk=submission_id)
    comp = sub.compileProfile
    problem = sub.problem
    test_cases = TestCase.objects.filter(problem__pk = problem.pk)
    limits = get_resource(sub, comp)       

    retval, stdout, stderr = compile(sub, comp)
    
    if retval:
        sub.text_feedback = 'Compile time error'
        return retval, stdout, stderr
    results = execute(sub, comp, test_cases, limits)
    exretval = 0
    for res in results:
        #No runtime error
        if res[0] == 0:
            exretval = res[0]
            sub.solved_problem = res[3]
            if sub.solved_problem:
                sub.text_feedback = "Solved"
            else:
                sub.text_feedback = "Wrong answer"
        #Runtime error
        else:
            exretval = res[0]
            sub.solved_problem = res[3]
            
            sub.text_feedback = "Evaluation timed out"
            break
    
    sub.save()
    print results
    return results

def compile(submission, compiler):
    #dir_path = WORK_ROOT + str(submission.id).strip()
    #command = 'cd ' + dir_path + ' && '+ compiler.compile
    dir_path, filename = os.path.split(submission.submission.path)
    command = re.sub(FILENAME_SUB, filename, compiler.compile)
    command = re.sub(BASENAME_SUB, filename.split('.')[0], command)
    args = shlex.split(command)
    process = Popen(args=args, stdout=PIPE, stderr=PIPE, cwd=dir_path)
    stdout, stderr = process.communicate()
    retval = process.poll()
    if os.path.exists(dir_path + '/' + filename.split('.')[0]):
        os.chmod(dir_path + '/' + filename.split('.')[0], 0751)
    else:
        print 'Cant find file'
    return retval, stdout, stderr
    
def execute(submission, compiler, test_cases, limit):
    #dir_path = WORK_ROOT + str(submission.id)
    #command = 'cd ' + dir_path + ' && ' + compiler.run
    #command = 'ulimit -t %d -v %d -u %d && ' % (limit.max_program_timeout, limit.max_memory, limit.max_processes)
    command = compiler.run
    dir_path, filename = os.path.split(os.path.abspath(submission.submission.path))
    command = re.sub(BASENAME_SUB, filename.split('.')[0], command)
    command = use_run_user(command)
                
    results = []
    for test in test_cases:
        test.inputFile.open("rb")
        test.outputFile.open("rb")
        input_content = test.inputFile.read()
        output_content= test.outputFile.read()
        test.inputFile.close()
        test.outputFile.close()
        #user_uid, user_gid = getUserData()
        
        args = shlex.split(command)
        process = Popen(args=args, stdin=PIPE, stdout=PIPE, stderr=PIPE,
                        preexec_fn=set_resource(limit.max_program_timeout, limit.max_memory, limit.max_processes),
                        cwd=dir_path)
        stdout, stderr = process.communicate(input_content)
        retval = process.poll()
        #retval, stdout, stderr = _run_safe_shell(command + ' < ' + str(test.inputFile.path))
        if stdout == output_content:
            results.append([retval, stdout, stderr, True])
        else:
            results.append([retval, stdout, stderr, False])
    
    #command += test_cases.
    return results

def run_test(submission, comp):
    dir_path = WORK_ROOT + submission.id
    command = 'cd ' + dir_path + ' && ' + comp.run_cmd
    re.sub(BASENAME_SUB, submission.submission.split(".")[0])

def base(filepath):
    return os.path.basename(filepath)


@app.task
def install_compilers(compilers):
    retval, stdout, stderr = _run_shell(["sudo apt-get update"])
    for compiler in compilers:
        retval, stdout, stderr = _run_shell("sudo apt-get install " + compiler.package_name)
        if retval:
            raise Exception(stderr)
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
    return 'sudo su ' + RUN_USER + ' -c "' + command + '"'

def _run_shell(command):
    runboy = Runner(command)
    runboy.run()
    
    return runboy.retval, runboy.out_stdout, runboy.out_stderr        
    
@app.task
def uname():
    retval, stdout, stderr = _run_shell("hostname")
    return stdout



 
