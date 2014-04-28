from __future__ import absolute_import
from openshift.execution.models import CompilerProfile, TestCase, Resource, get_resource
from openshift.teamsubmission.models import Submission, ExecutionLogEntry 
from subprocess import call
from openshift import celery_app as app
from subprocess import PIPE, Popen
from signal import SIGKILL, SIGXCPU, SIGALRM, alarm, signal 
from django.utils.encoding import smart_str, smart_bytes
from psutil import AccessDenied
import re
import os
import shlex
import resource
import logging
import psutil
import subprocess

logger = logging.getLogger('idiopen')

WORK_ROOT   = "/idiopen/work/"
FILENAME    = "sauce.in"
FILENAME_SUB = "{FILENAME}"
BASENAME_SUB = "{BASENAME}"

RUN_USER = "gentlemember"

REALTIME_MULTIPLIER = 3

STDOUT_MAX_SIZE = 512*1024
STDERR_MAX_SIZE = 512*1024


#Categorization of exit codes. 
USER_TIMEOUT    = [137, 35072]
USER_CRASH      = [1,9,128,257,300]
PROC_EXCEED     = [139]
MEM_EXCEED      = [-9,134]

def set_resource(time, memory=-1, procs=-1):
    '''
    Return a function that sets resources for a subprocess
    -1 is equivalent to unlimited, or os max limits. The funtion will also set nice to 19 for the process

    Keyword arguments:
    time -- maximum cpu time in seconds
    memory -- maximum memory in bytes (default -1)
    procs -- maximum processes (default -1)
    '''
    def result():
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
	'''
	Entry point for submission evaluation. Sets up a RunJob instance for the submitted source and goes through the stages of compiling the submission,
	running the compiled subsmission through all related test_cases and finally evaluating the results.  
	'''
    submission  = Submission.objects.get(pk=submission_id)
    #try:
    compiler    = submission.compileProfile
    problem     = submission.problem
    submission.status = Submission.RUNNING
    submission.save()
    runner = RunJob(submission.submission, 
                           compiler, 
                           get_resource(submission, compiler))
    
    retval, stdout, stderr = runner.compile()
    runLogger(submission, runner.compileCMD, stdout, stderr, retval)
    if retval != 0:
        if retval in MEM_EXCEED:
            submission.text_feedback = "Compile time memory limit exceeded."
        elif retval in USER_TIMEOUT:
            submission.text_feedback = "Compile timeout"
        else:
            submission.text_feedback = "Compile time error."
        submission.status = Submission.EVALUATED
        submission.save()
        return retval, stdout, stderr

    logger.debug('Exec start')

    results = run_tests(runner, submission)
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
                submission.text_feedback = "Runtime error."   
            break
    logger.debug('Exec end')
    submission.status = Submission.EVALUATED
    submission.save()
    return results
    #except Exception as e:
    #    logger.debug(e.args)
    #    logger.debug(e.message)
    #    submission.status = Submission.EVALUATED
    #    submission.text_feedback = "Something went wrong. Contacts admins"
    #    submission.save()


class RunJob():
    '''
    Class that compiles and runs the given sourcefile
    '''
    def __init__(self, sourceFile, compilerProfile, limit):
        self.dir_path, self.filename = os.path.split(os.path.abspath(sourceFile.path))
        self.compiler   = compilerProfile
        self.file       = sourceFile
        self.compileCMD = self.cmd_replace(compilerProfile.compile)
        self.runCMD     = self.cmd_replace(compilerProfile.run)
        self.limit      = limit

    def compile(self):
        resource = set_resource(self.limit.max_compile_time)
        
        if not self.compileCMD:
            return 0,'',''
        
        retval, stdout, stderr = execute(self.compileCMD, 
                                     self.dir_path, 
                                     resource,
                                     timeout=self.limit.max_compile_time*REALTIME_MULTIPLIER)
    
        if os.path.exists(self.dir_path + '/' + self.filename.split('.')[0]):
            os.chmod(self.dir_path + '/' + self.filename.split('.')[0], 0751)
        else:
            logger.debug('Cant find executable')
     
        return retval, stdout, stderr
        
    def run(self, stdin, restricted=True, timed=True):
        command = self.runCMD
        if timed:
            command = time_command(command)
        if restricted:
            command = use_run_user(command)
            
        timeout = self.limit.max_program_timeout
        resource = set_resource(timeout, 
                                MBtoB(self.limit.max_memory), 
                                self.limit.max_processes)
        retval, stdout, stderr = execute(command, 
                                         self.dir_path, 
                                         resource, 
                                         stdin, 
                                         timeout=timeout*REALTIME_MULTIPLIER)
        return retval, stdout, stderr, command
    
    
    def cmd_replace(self, command):
        command = re.sub(FILENAME_SUB, self.filename, command)
        command = re.sub(BASENAME_SUB, self.filename.split('.')[0], command)
        return command
    
def run_tests(runJob, submission):
	'''
	run_tests goes through all the test cases related to the problem the submission is intended to solve.
	Runnning a test case consists of running the submission with an input given by the test case. The next 
	step is to check whether or not the output from the run was valid. This can be done either by means of
	a custom validator, or simply by doing a simple string comparison with the correct output (provided by
	the test case). 
	'''
    test_cases = TestCase.objects.filter(problem__pk = submission.problem.pk)
    results = []
    for test in test_cases:
        test.inputFile.open("rb")
        test.outputFile.open("rb")
        input_content = test.inputFile.read()
        output_content= test.outputFile.read()
        test.inputFile.close()
        test.outputFile.close()
        
        retval, stdout, stderr, command = runJob.run(input_content)
        runLogger(submission, command, stdout, stderr, retval)
                                        
        try:
            lines = [x for x in stderr.split("\n") if x != '']
            time = lines[-1]
            usertime, systime = time.split('n')
            submission.runtime = (float(usertime) + float(systime))* 1000
        except (ValueError, IndexError):
            results.append([retval, stdout, stderr, False])
            continue

        if test.validator:
            if validate(input_content, stdout, test):
                results.append([retval, stdout, stderr, True])
            else:
                results.append([retval, stdout, stderr, False])
        else:
            if stdout==output_content:
                results.append([retval, stdout, stderr, True])
            else:
                results.append([retval, stdout, stderr, False])
   
    return results

def get_validator_resource():
    '''
    Returns a resource object for use with validators
    '''
    resource = Resource()
    resource.max_compile_time = 20
    resource.max_filesize = 50
    resource.max_memory = -1
    resource.max_processes = -1
    resource.max_program_timeout = 50
    return resource



def MBtoB(mbcount):
    if mbcount == -1:
        return mbcount
    return mbcount*(1024**2)


def validate(input_content, run_stdout, test_case):
	'''
	Uses a custom validator to check whether or not the output from a test run is correct.
	The first step is to compile the validator, then run it with the concatenation of the 
	test case input and the output from the submission test run.
	'''
    
    runner = RunJob(test_case.validator, test_case.compileProfile, get_validator_resource())
    retval, stdout, stderr = runner.compile()

    if retval:
        return False

    retval, stdout, stderr, command = runner.run(input_content+run_stdout,restricted=False, timed=False) 
    try:
        return int(stdout) == 1
    except:
        return False

def runLogger(submission, command, stdout, stderr, retval):
    '''
    Creates a ExecutionLogEntry for the given parameters.
    It will also limit stdout and stderr to 512kB
    '''
    if len(smart_bytes(stdout, errors="replace")) > STDOUT_MAX_SIZE:
        stdout = 'stdout to large'
    if len(smart_bytes(stderr, errors="replace")) > STDERR_MAX_SIZE:
        stderr = 'stderr to large'
    ExecutionLogEntry.objects.create(submission=submission,
                                    command=command,
                                    stdout=stdout,
                                    stderr=stderr,
                                    retval=retval).save()

def execute(command, dir_path, res, stdin=None, timeout = -1):
    '''
    Will execute the given command

    Keyword arguments:
    command -- the command to be executed
    dir_path -- the location where the command should be executed
    res -- the resource function to the applied before the command is executed
    stdin -- the input that should be piped to the command (default None)
    timeout -- When the process and all of its children should be killed (default -1)
    '''
    class Alarm(Exception):
        pass
    def alarm_handler(signum, frame):
        raise Alarm
    args = shlex.split(command) # Split command based on os?
    logger.debug(args)
    process = psutil.Popen(args=args, 
                           stdin=PIPE, stdout=PIPE, stderr=PIPE,
                           preexec_fn=res,
                           cwd=dir_path)
    if timeout != -1: # If there should be a timeout
        signal(SIGALRM, alarm_handler) # Catch SIGALRM and call alarm_handler
        alarm(timeout) # Will call SIGALRM after timeout
    try:
        stdout, stderr = process.communicate(stdin) # Communicates stdin and waits for the process to end
        if timeout != -1:
            alarm(0)
    except Alarm: # If the alarm is trigered it will kill all children
        procs = (process.children(recursive=True)) # Gets all children recursively
        pids = [str(proc.pid) for proc in procs] 
        try:
            logger.debug('KILLING')
            cmd = shlex.split('sudo kill ' + ' '.join(pids))
            subprocess.call(cmd)
        except OSError, psutil.AccessDenied: # May not get these exceptions
            pass
        return 137, '', '0.0n0.0'      
    retval = process.poll()
    return retval, stdout, stderr

def use_run_user(command):
	'''
	Used to run submissions as a less privileged user than the one doing compilation. 
	'''
    return 'sudo su ' + RUN_USER + ' -c "' + command + '"'

def time_command(command):
	'''
	Used to get the runtime of a test run.
	'''
    return '/usr/bin/time -f "%Sn%U" -q ' + command

