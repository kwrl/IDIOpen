from locust import HttpLocust, TaskSet, task

from random import randint

files = [open('test.java', 'r'), open('test2.java', 'r')]
usernames = open('emails.txt', 'r').read()
usernames = usernames.split('\n')[::-1]
usernames.pop()

class NestTask(TaskSet):
    @task
    class SubmissionTask(TaskSet):
        def on_start(self):
            loginDict = {
                    'username': 'test@test.no',
                    'password': 'test123',
                    }

            c = self.client.post("/open14/accounts/login/", loginDict)

        @task
        def upload_submission(self):
            submission_json = {
                    'compileProfile': {'1'},
                    }
            file_upload = files[randint(0, len(files) -1)]

            file_json = {
                        'submission' : file_upload,
                        }

            c = self.client.post("/open14/problem/1/", submission_json,
                                 files=file_json)
            print c.content

    @task
    class RegistrationTask(TaskSet):
        @task
        def register(self):
            global usernames
            postDict = {
                    'email'       : usernames.pop(),
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
    min_wait = 5000 #
    """ maximum wait before executing a task"""
    max_wait = 15000 #
    """ Weight, how often to run task relative to others"""
    weight = 3

    """ the target, as a prefix """
    #host = "http://127.0.0.1:8000"
    host = "http://vps.filip0.com"

# EOF

