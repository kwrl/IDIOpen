""" You need trailing slashes in all URLS
"""

from locust import HttpLocust, TaskSet, task

from os import walk
import sys
from random import randint


ALL_SUBS = [(path, lol, file) for path, lol, file in walk("subfiles")][0][2]
FILETYPES = [".java", ".cpp", "c"]
FILES_PREFIX = "./subfiles/"
def get_files(extension, fileList=ALL_SUBS):
    return [open(FILES_PREFIX + filename, 'r') for filename in ALL_SUBS \
                                        if extension in ALL_SUBS]



JAVA_FILES = get_files(".java")
C_FILES = get_files(".java")
CPP_FILES = get_files(".java")
files = JAVA_FILES

USERNAME_LIST = open('emails.txt', 'r').read()
USERNAME_LIST = USERNAME_LIST.split('\n')
USERNAME_LIST.pop()
USERNAME_LIST = USERNAME_LIST[::-1]

PROBLEMS = [1, 6, 7, 8, 11, 12, 13, 14, 17, 18, 19, 21, 22]

class NestTask(TaskSet):
    #@task
    class SubmissionTask(TaskSet):
        def on_start(self):
            global USERNAME_LIST
            user = USERNAME_LIST[randint(0, len(USERNAME_LIST)-1)]
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
            file_upload = files[randint(0, len(JAVA_FILES) -1)]

            file_json = {
                        'submission' : file_upload,
                        }

            problem = PROBLEMS[randint(0, len(PROBLEMS)-1)]
            c = self.client.post("/open14/problem/" + str(problem) + "/", submission_json,
                                 files=file_json)
            print c.content

    #@task
    class RegisterTeam(TaskSet):
        global USERNAME_LIST
        user = USERNAME_LIST[randint(0, len(USERNAME_LIST)-1)]
        #user = USERNAME_LIST.pop()

        def on_start(self):
            #global USERNAME_LIST
            #user = USERNAME_LIST[randint(0, len(USERNAME_LIST)-1)]
            #user = self.user
            loginDict = {
                    'username': self.user,
                    'password': 'password',
                    }

            c = self.client.post("/open14/accounts/login/", loginDict)

        @task
        def registerTeam(self):
            """
            """
            # Strip away ".com" and remove the at and period mark
            teamname = "team" + self.user.translate(None, '@.')[:-3]
            teamurl = "/open14/team/register/"
            postDict = {
                    'name'       : teamname,
                    'onsite'     : 'True',
                    'member_two' : '',
                    'member_one' : '',
                }

            c = self.client.post(teamurl, postDict)
            #self.interrupt(reschedule=False)
            sys.exit(0)

    @task
    class RegisterUser(TaskSet):
        global USERNAME_LIST
        user = USERNAME_LIST[randint(0, len(USERNAME_LIST)-1)]
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

            c = self.client.post("/open14/accounts/register/",
                    data=postDict)
            self.interrupt()

    @task
    class GetUrls(TaskSet):
        
        def on_start(self):
            loginDict = {
                        'username': 'idi@open.no',
                        'password': 'idiopen',
                    }
            c = self.client.post("/open14/accounts/login/", loginDict)

        @task
        def getHighScore(self):
            c = self.client.get("/open14/highscore/")
        
        @task
        def getContestView(self):
            c = self.client.get("/open14/problem/")

        @task
        def getClarifications(self):
            c = self.client.get("/open14/problem/answers/")

        @task
        def getTeamView(self):
            c = self.client.get("/open14/team/")

        @task
        def getProfileView(self):
            c = self.client.get("/open14/accounts/profile/")

        @task
        def getTeamsView(self):
            c = self.client.get("/open14/teams/")

#Admin site
        @task
        def getBalloonView(self):
            c = self.client.get("/admin/balloon/balloon_view/")

        @task
        def getJudgeView(self):
            c = self.client.get("/admin/judge_supervise/judge_view/")


class WebsiteUser(HttpLocust):
    """ Emulate a real user browsing the pages.
    """
    task_set = NestTask
    """ minimum wait before doing a task as a user """
    min_wait = 1000 #
    """ maximum wait before executing a task"""
    max_wait = 3000 #
    """ Weight, how often to run task relative to others"""
    weight = 3

    """ the target, as a prefix """
    #host = "http://127.0.0.1:8000"
    host = "http://vps.filip0.com"

# EOF
