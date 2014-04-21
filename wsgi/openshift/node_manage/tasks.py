from __future__ import absolute_import
from openshift.execution.models import CompilerProfile, TestCase, Resource, get_resource
from openshift.teamsubmission.models import Submission, ExecutionLogEntry 
from subprocess import call
from openshift import celery_app as app
from subprocess import PIPE, Popen
from signal import SIGKILL, SIGXCPU 
import re
import os
import threading
import time
import pwd
import shlex
import resource
import logging

logger = logging.getLogger('idiopen')

WORK_ROOT   = "/idiopen/work/"
FILENAME    = "sauce.in"
FILENAME_SUB = "{FILENAME}"
BASENAME_SUB = "{BASENAME}"

RUN_USER = "gentlemember"

USER_TIMEOUT    = [137, 35072]
USER_CRASH      = [1,9,128,257,300]
PROC_EXCEED     = [11, 139]
MEM_EXCEED      = [-9]

def set_resource(time, memory, procs):
    def result():
        memory  = memory*(1024**2)
        nproc   = resource.getrlimit(resource.RLIMIT_NPROC)
        tcpu    = resource.getrlimit(resource.RLIMIT_CPU)
        mem     = resource.getrlimit(resource.RLIMIT_DATA)
        # Set The maximum number of processes the current process may create.
        try:
            resource.setrlimit(resource.RLIMIT_NPROC, (procs, procs))
        except Exception:
            resource.setrlimit(resource.RLIMIT_NPROC, nproc)
            
        # Set The maximum amount of processor time (in seconds) that a process can use.
        try:
            resource.setrlimit(resource.RLIMIT_CPU, (time, time))
        except Exception:
            resource.setrlimit(resource.RLIMIT_CPU, tcpu)

        # Set The maximum area (in bytes) of address space which may be taken by the process.
        try:
            resource.setrlimit(resource.RLIMIT_AS, (memory, memory))
        except Exception:
            resource.setrlimit(resource.RLIMIT_AS, mem)
    
        os.nice(19)
    return result
    #limit.max_program_timeout, limit.max_memory, limit.max_processes

@app.task
def evaluate_task(submission_id):
    submission  = Submission.objects.get(pk=submission_id)
    compiler    = submission.compileProfile
    problem     = submission.problem
    submission.status = Submission.RUNNING
    submission.save()
    retval, stdout, stderr = compile_submission(submission)
    if retval != 0:
        if retval in MEM_EXCEED:
            submission.text_feedback = "Compile time memory limit exceeded."
        elif retval in USER_TIMEOUT:
            submission.text_feedback = "Compile timeout"
        else:
            submission.text_feedback = "Unspecified compile time error."
        
        submission.save()
        return retval, stdout, stderr

    logger.debug('Exec start')

    results = run_tests(submission)
    exretval = 0

    for res in results:
        #No runtime error
        if res[0] == 0:
            exretval = res[0]
            submission.solved_problem = res[3]
            if submission.solved_problem:
                submission.text_feedback = "Successful submission!"
            else:
                submission.text_feedback = "Incorrect output."
        #Runtime error
        else:
            exretval = res[0]
            submission.solved_problem = res[3]
            
            if exretval in MEM_EXCEED:
                submission.text_feedback = "Runtime memory limit exceeded."
            elif exretval in USER_TIMEOUT:
                submission.text_feedback = "Runtime timeout."
            elif exretval in PROC_EXCEED:
                submission.text_feedback = "Number of processes exceeded."
            else:
                submission.text_feedback = "Unspecified runtime error."   
            break
    logger.debug('Exec end')
    submission.status = Submission.EVALUATED
    submission.save()
    return results

def compile_submission(submission):
    compiler = submission.compileProfile
    limits = get_resource(submission, compiler)
    command = compiler.compile
    retval, stdout, stderr = compile(compiler, limits, submission.submission.path)
    
    ExecutionLogEntry.objects.create(submission=submission, 
                                            command=command, 
                                            stdout=stdout, 
                                            stderr=stderr,
                                            retval=retval).save()
    
    return retval, stdout, stderr

def compile_validator(test_case):
    compiler = test_case.compileProfile
    resource = set_resource(-1,-1,-1)

    return compile( compiler,
                    get_validator_resource(),
                    test_case.validator.path)

def get_validator_resource():
    resource = Resource()
    resource.max_compile_time = 20
    resource.max_filesize = 50
    resource.max_memory = -1
    resource.max_processes = -1
    resource.max_program_timeout = 50
    return resource

def compile(compiler, limits, sourcepath):
    dir_path, filename = os.path.split(sourcepath)
    command = re.sub(FILENAME_SUB, filename, compiler.compile)
    command = re.sub(BASENAME_SUB, filename.split('.')[0], command)
    
    retval, stdout, stderr =   run( command, dir_path, set_resource(
                                    limits.max_program_timeout,
                                    -1,
                                    -1), "")

    if os.path.exists(dir_path + '/' + filename.split('.')[0]):
        os.chmod(dir_path + '/' + filename.split('.')[0], 0751)
    else:
        logger.debug('Cant find executable')
 
    return retval, stdout, stderr

def run_tests(submission):
    command = get_submission_run_cmd(submission)
    compiler = submission.compileProfile
    limit = get_resource(submission,compiler)
    limit.max_processes += 10
    dir_path, filename = os.path.split(os.path.abspath(submission.submission.path))
    test_cases = TestCase.objects.filter(problem__pk = submission.problem.pk)
    results = []
    for test in test_cases:
        test.inputFile.open("rb")
        test.outputFile.open("rb")
        input_content = test.inputFile.read()
        output_content= test.outputFile.read()
        test.inputFile.close()
        test.outputFile.close()
        
        retval, stdout, stderr = run(command, dir_path, set_resource(
                                        limit.max_program_timeout,
                                        limit.max_memory,
                                        limit.max_processes),
                                        input_content)       
        
        ExecutionLogEntry.objects.create(submission=submission, 
                                            command=command, 
                                            stdout=stdout, 
                                            stderr=stderr,
                                            retval=retval).save()
 
        try:
            lines = stderr.split("\n")
            lines = [x for x in lines if x != '']  
            usertime= float(lines[-1])
            systime = float(lines[-2])
            submission.runtime = (usertime + systime)* 1000
            stderr = '\n'.join(lines)
        except ValueError:
            results.append([retval, stdout, stderr, False])
            continue

        if test.validator:
            if validate(stdout, test):
                results.append([retval, stdout, stderr, True])
            else:
                results.append([retval, stdout, stderr, False])
        else:
            if stdout==output_content:
                results.append([retval, stdout, stderr, True])
            else:
                results.append([retval, stdout, stderr, False])
   
    return results

def get_submission_run_cmd(submission):
    compiler    = submission.compileProfile
    limit       = get_resource(submission, submission.compileProfile)
   
    command = compiler.run
    dir_path, filename = os.path.split(os.path.abspath(submission.submission.path))
    command = re.sub(BASENAME_SUB, filename.split('.')[0], command)
   
    command = use_run_user(command)
    command = time_command(command)
    
    return command

def get_validator_run_cmd(test_case):
    compiler = test_case.compileProfile
    dir_path, filename = os.path.split(test_case.validator.path)
    return re.sub(BASENAME_SUB, filename.split('.')[0], compiler.run)

def validate(run_stdout, test_case):
    retval, stdout, stderr = compile_validator(test_case)

    dir_path, filename = os.path.split(os.path.abspath(test_case.validator.path))
    command = get_validator_run_cmd(test_case)
    if retval:
        return False

    limits = get_validator_resource()
    res = set_resource(limits.max_program_timeout,limits.max_memory,limits.max_processes)

    retval, stdout, stderr = run(command, dir_path, res, run_stdout) 

    return retval==0 

def run(command, dir_path, resource, stdin):
    args = shlex.split(command)
    logger.debug(args)

    process = Popen(args=args, stdin=PIPE, stdout=PIPE, stderr=PIPE,
                preexec_fn=resource,
                cwd=dir_path)

    stdout, stderr = process.communicate(stdin)
    retval = process.poll()

    return retval, stdout, stderr

def use_run_user(command):
    return 'sudo su ' + RUN_USER + ' -c "' + command + '"'

def time_command(command):
    return '/usr/bin/time -f "%S\n%U" -q ' + command

