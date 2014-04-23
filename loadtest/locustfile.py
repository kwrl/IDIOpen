#! /home/andesil/pyenv/bin/python

from locust import HttpLocust, TaskSet, task, ResponseError

class RegistrationTask(TaskSet):
    @task
    def register(self):
        postDict = {
                'email'       : 'and@sild.com',
                'first_name'  : 'anders',
                'last_name'   : 'sildnes',
                'nickname'    : 'nick',
                'password1'   : 'password',
                'password2'   : 'password',
                'skill_level' : '1',
                'gender'      : 'M',
                }
        c = self.client.post("/open14/accounts/register/",
                              postDict)
        print c
        print c.content

class SubmissionTask(TaskSet):
	def on_start(self):
		loginDict = {
			'username': 'admin@gmail.com',
			'password': 'admin123',
			}
			
		c = self.client.post("/open14/accounts/login/", loginDict)

	#@task(1)
	def example_get(self):
		self.client.get("/open14/team/")

	@task(1)
	def upload_submission(self):
		subDict = {
			'compileProfile': '1',
			'submission' : """class Test{public static void main(String[] args) { }}""",
		}
		c = self.client.post("/open14/accounts/login/", loginDict)
		print c.content


           
class WebsiteUser(HttpLocust):
    """ Emulate a real user browsing the pages.
    """
    #task_set = WebsiteTasks
    #task_set = RegistrationTask
    task_set = SubmissionTask
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
