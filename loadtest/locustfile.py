""" You need trailing slashes in all URLS
"""

from locust import HttpLocust, TaskSet, task

from os import walk
from random import randint

files = [open('subfiles/test.java', 'r'), open('subfiles/test2.java', 'r'), open('subfiles/angry_rs.java', 'r')]
ffiles = [(path, lol, file) for path, lol, file in os.walk("subfiles")][0][2]
javafiles= [java for java in ffiles if "java" in java]


usernames = open('emails.txt', 'r').read()
usernames = usernames.split('\n')
usernames.pop()

problems = [1, 6, 7, 8, 11, 12, 13, 14, 17, 18, 19, 21, 22]

class NestTask(TaskSet):
    @task
    class SubmissionTask(TaskSet):
        def on_start(self):
            global usernames
            user = usernames[randint(0, len(usernames)-1)]
            loginDict = {
                    'username': user,
                    'password': 'password',
                    }

            c = self.client.post("/open14/accounts/login/", loginDict)

        @task
        def upload_submission(self):
            submission_json = {
                    'compileProfile': {'1'},
                    }
            file_upload = files[randint(0, len(javafiles) -1)]

            file_json = {
                        'submission' : file_upload,
                        }

            problem = problems[randint(0, len(problems)-1)]
            c = self.client.post("/open14/problem/" + str(problem) + "/", submission_json,
                                 files=file_json)
            print c.content

    #@task
    class RegisterTeam(TaskSet):
        global usernames
        #user = usernames[randint(0, len(usernames)-1)]
        user = usernames.pop()

        def on_start(self):
            global usernames
            user = usernames[randint(0, len(usernames)-1)]
            #user = self.user
            loginDict = {
                    'username': user,
                    'password': 'password',
                    }

            c = self.client.post("/open14/accounts/login/", loginDict)

        @task
        def registerTeam(self):
            """
            """
            # Strip away ".com" and remove the at and period mark
            #teamname = "team" + self.user.translate(None, '@.')[:-3]
            teamname = "team" + self.user.translate(None, '@.')[:-3]
            #teamname = "team" + usernames[randint(0, len(usernames)-1)]
            teamurl = "/open14/team/register/"
            postDict = {
                    'name'       : teamname,
                    'onsite'     : 'True',
                    'member_two' : '',
                    'member_one' : '',
                }

            c = self.client.post(teamurl, postDict)
            self.interrupt(reschedule=True)


    #@task
    class RegisterUser(TaskSet):
        global usernames
        user = usernames[randint(0, len(usernames)-1)]
        #@task
        def registerUser(self):
            postDict = {
                    'email'       : self.user,
                    'first_name'  : 'first',
                    'last_name'   : 'last',
                    'nickname'    : 'nick',
                    'password1'   : 'password',
                    'password2'   : 'password',
                    'skill_level' : '1',
                    'gender'      : 'M',
                    }

            c = self.client.post("/open14/accounts/register/",
                    data=postDict)
            #print c
            print c

        
class WebsiteUser(HttpLocust):
    """ Emulate a real user browsing the pages.
    """
    #task_set = WebsiteTasks
    #task_set = RegistrationTask
    task_set = NestTask
    """ minimum wait before doing a task as a user """
    min_wait = 10000 #
    """ maximum wait before executing a task"""
    max_wait = 15000 #
    """ Weight, how often to run task relative to others"""
    weight = 3

    """ the target, as a prefix """
    #host = "http://127.0.0.1:8000"
    host = "http://vps.filip0.com"

# EOF

