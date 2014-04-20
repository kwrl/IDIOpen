#! /home/andesil/pyenv/bin/python

from locust import HttpLocust, TaskSet, task, ResponseError

class WebsiteTasks(TaskSet):
    def on_start(self):
        self.client.post("/login", {
            "username": "test_user",
            "password": ""
        })

    #@task
    def getRange(self):
        # Statistics for these requests will be grouped under: /blog/?id=[id]
        for i in range(10):
            client.get("/blog?id=%i" % i, name="/blog?id=[id]")
    
    @task
    def index(self):
        self.client.get("/")
        
    #@task
    def about(self):
        self.client.get("/about/")

    @task
    def testTask(self):
        with self.client.get("/", catch_response=True) as response:
            if response.content != "Success":
                response.failure("Got wrong response")

class RegistrationTask(TaskSet):
    def on_start(self):
        pass
           
    @task
    def register(self):
        postDict = {
                'email'       : 'and@sild.com',
                'first_name'  : 'anders',
                'last_name'   : 'sildnes',
                'nickname'    : 'nick',
                'password1'   : 'pass',
                'password2'   : 'pass',
                'skill_level' : '1',
                'gender'      : 'M',
                }
        with self.client.post("/adw/accounts/register",
                              postDict, 
                              catch_response=True) \
            as response:
                if response.data == "fail":
                    raise ResponseError("Invalid feedback")
                else:
                    print "aaa"





class WebsiteUser(HttpLocust):
    """ Emulate a real user browsing the pages.
    """
    #task_set = WebsiteTasks
    task_set = RegistrationTask
    """ minimum wait before doing a task as a user """
    min_wait = 5000 # 
    """ maximum wait before executing a task"""
    max_wait = 15000 # 
    """ Weight, how often to run task relative to others"""
    weight = 3 

    """ the target, as a prefix """
    host = "http://127.0.0.1:8000"

"""

&email=email%40email.com&firs
t_name=FIRST&last_name=NAME&nickname=NICK&password1=PASS&password2=PASS&skill_lev
el=Pro&gender=M  
"""

# EOF
