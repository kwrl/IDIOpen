import os
import popen2
import re
import threading
import time
import random
import sys
import ipdb

RUN_SERVER_DIR  = '/tmp/run_server'
QUEUE_FILE      = RUN_SERVER_DIR + '/queue'
LOG_FILE        = RUN_SERVER_DIR + '/log.txt'
ERRLOG_FILE     = RUN_SERVER_DIR + '/errlog.txt'
RUN_USER        = 'algrun'

MAX_COMPILE_TIME    = 30.0
MIN_RUN_REPEATS     = 1
MAX_RUN_REPEATS     = 10
MIN_PROGRAM_TIMEOUT = 1
MAX_PROGRAM_TIMEOUT = 60

# This is used in addition to usertime timeout, in case of sleeping programs
DEAD_PROGRAM_TIMEOUT    = 2 * MAX_PROGRAM_TIMEOUT # Watch for old "dead" runs
MAX_MEM                 = 100000 # kilobytes
MEM_JAVA_ADDITION       = 200000 # sun java is greedy
MAX_PROC                = 5 # maximum number of child processes (avoid fork bombs)

PROC_JAVA_ADDITION_VALIDATOR    = 9
PROC_JAVA_ADDITION_PROGRAM      = 7
MAX_OUTPUT_SIZE                 = 1000000
SEPARATE_RUN_THREAD             = False # or let _kill_old_and_dead() clean house
DO_LOG                          = True

FILENAME_SUB = "{FILENAME}"
BASENAME_SUB = "{BASENAME}"

class CompilerProfile:
    def __init__(self, name, extensions, compiler_cmd, compiler_flags, run_cmd, run_flags, package_name):
        self.name               = name
        self.extensions         = extensions
        self.compiler_cmd       = compiler_cmd
        self.compiler_flags     = compiler_flags
        self.run_cmd            = run_cmd
        self.run_flags          = run_flags
        self.package_name       = package_name
 
    def __unicode__(self):
        return self.name

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

class Submission:
    def __init__(self, directory, filename, basename, timeout):
        self.directory  = directory
        self.filename   = filename
        self.basename   = basename
        self.timeout    = timeout
        self.max_proc   = 10

class TestCase:
    def __init__(self, input_content, output_content):
        self.input_content  = input_content
        self.output_content = output_content


#TODO implement restrictions
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

def use_run_user(command):
    return 'nice sudo su ' + RUN_USER + ' -c "' + command + '"' 

def create_temp_dir(dir_parent):
    temp_dir = '%s/tmp_run_%f_%d_%d' % (dir_parent, time.time(), os.getpid(), random.randint(0,sys.maxint))

    if os.path.exists(temp_dir):
        raise Exception("NASTY ERROR: Temp directory %s already existed")

    os.mkdir(temp_dir)
    os.chmod(temp_dir, 0711)

    return temp_dir

def remove_temp_dir(temp_dir):
    for f in  os.listdir(temp_dir):
        os.unlink(temp_dir + '/' + f)
    os.rmdir(temp_dir)

def compile(submission, compiler):
    command = 'cd ' + submission.directory + ' && ' + compiler.compiler_cmd  
    command = compiler.compiler_cmd
    command = re.sub(FILENAME_SUB, submission.filename, command)
    command = re.sub(BASENAME_SUB, submission.basename, command)
    return _run_shell(submission.timeout, command, False) 
    

def run(submission, compiler):
    command = compiler.run_cmd
    command = re.sub(BASENAME_SUB, submission.basename, command)
    return _run_shell(submission.timeout, command, False) 

def run_test(submission, compiler, test):
    command = compiler.run_cmd
    command = re.sub(BASENAME_SUB, submission.basename, command)
    command += ' ' + test.input_content
    retval, stdout, stderr =_run_safe_shell(submission.timeout, command, False)
    
    if retval != 0:
        raise Exception("Runtime error")   
 
    return is_valid(stdout, test.output_content)
    
def is_valid(out, correct):
    pass









