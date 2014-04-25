""" You need trailing slashes in all URLS
"""
from locust import TaskSet, task, HttpLocust, Locust

from os import walk

import sys
from random import randint


ALL_SUBS = [(path, lol, file) for path, lol, file in walk("./subfiles")][0][2]
FILETYPES = [".java", ".cpp", "c"]
FILES_PREFIX = "./subfiles/"
def get_files(extension, fileList=ALL_SUBS):

    return [open(FILES_PREFIX + filename, 'r') for filename in ALL_SUBS \
                                        if extension in filename]

JAVA_FILES = get_files("java", ALL_SUBS)
C_FILES = get_files(".java")
CPP_FILES = get_files(".java")
files = JAVA_FILES
USERNAME_LIST = open('emails.txt', 'r').read()
USERNAME_LIST = USERNAME_LIST.split('\n')
USERNAME_LIST.pop()
USERNAME_LIST = USERNAME_LIST[::-1]

PROBLEMS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

class NestTask(TaskSet):
    #@task
    class SubmissionTask(TaskSet):
        def on_start(self):
            global USERNAME_LIST
            # user = USERNAME_LIST[randint(0, len(USERNAME_LIST)-1)]
            self.user = USERNAME_LIST.pop()
            loginDict = {
                    'username': self.user,
                    'password': 'password',
                    }

            c = self.client.post("/secrettest/accounts/login/", loginDict)

        @task
        def upload_submission(self):
            submission_json = {
                    'compileProfile': {'1'},
                    }
            file_upload = files[randint(0, len(JAVA_FILES) -1)]

            file_json = {
                        'submission' : file_upload,
                        }

            problem = PROBLEMS[randint(0, len(PROBLEMS)-1)]
            c = self.client.post("/secrettest/problem/" + str(problem) + "/", submission_json,
                                 files=file_json)
            print c.content

    #@task
    class RegisterTeam(TaskSet):
        global USERNAME_LIST
        #user = USERNAME_LIST.pop()

        def on_start(self):
            #global USERNAME_LIST
            #user = USERNAME_LIST[randint(0, len(USERNAME_LIST)-1)]
            #user = self.user
            self.user = USERNAME_LIST.pop()
            loginDict = {
                    'username': self.user,
                    'password': 'password',
                    }

            c = self.client.post("/secrettest/accounts/login/", loginDict)

        @task
        def registerTeam(self):
            """
            """
            # Strip away ".com" and remove the at and period mark
            teamname = "team" + self.user.translate(None, '@.')[:-3]
            teamurl = "/secrettest/team/register/"
            postDict = {
                    'name'       : teamname,
                    'onsite'     : 'True',
                    'member_two' : '',
                    'member_one' : '',
                }

            c = self.client.post(teamurl, postDict)
            print c.content
            self.interrupt()

    #@task
    class RegisterUser(TaskSet):
        global USERNAME_LIST
        # user = USERNAME_LIST[randint(0, len(USERNAME_LIST)-1)]
        def on_start(self):
            self.user = USERNAME_LIST.pop()

        @task
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

            c = self.client.post("/secrettest/accounts/register/",
                    data=postDict)
            self.interrupt()

    @task
    class GetUrls(TaskSet):
        
        def on_start(self):
            loginDict = {
                        'username': 'haakon.konrad@gmail.com',
                        'password': 'penis123',
                    }
            c = self.client.post("/secrettest/accounts/login/", loginDict)

        @task
        def getHighScore(self):
            c = self.client.get("/secrettest/highscore/")
        
        @task
        def getContestView(self):
            c = self.client.get("/secrettest/problem/")

        @task
        def getClarifications(self):
            c = self.client.get("/secrettest/problem/answers/")

        @task
        def getTeamView(self):
            c = self.client.get("/secrettest/team/")

        @task
        def getProfileView(self):
            c = self.client.get("/secrettest/accounts/profile/")

        @task
        def getTeamsView(self):
            c = self.client.get("/secrettest/teams/")
        
        #@task
        def getProblemView(self):
            c = self.client.get("/secrettest/problem/1/")
            
#Admin site
        @task
        def getBalloonView(self):
            c = self.client.get("/admin/balloon/balloon_view/")

        #@task
        def getJudgeView(self):
            c = self.client.get("/admin/judge_supervise/judge_view/")


class WebsiteUser(HttpLocust):
    """ Emulate a real user browsing the pages.
    """
    task_set = NestTask
    """ minimum wait before doing a task as a user """
    min_wait = 10000 #
    """ maximum wait before executing a task"""
    max_wait = 20000 #
    """ Weight, how often to run task relative to others"""
    weight = 3

    """ the target, as a prefix """
    #host = "http://127.0.0.1:8000"
    #host = "http://vps.filip0.com"
    host = "http://hv-6146.idi.ntnu.no"

# EOF
