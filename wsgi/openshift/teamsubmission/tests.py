from django.test import TestCase
from .models import Submission
from .forms import SubmissionForm
 

from openshift.execution.models import Problem, CompilerProfile
from openshift.contest.models import Contest, Link, Team
import datetime
from django.contrib.sites.models import Site
from openshift.userregistration.models import CustomUser

# Create your tests here.

class submissionTestCase(TestCase):
    
    
    #===========================================================================
    # From userregistration.test. Modified by Typo
    #===========================================================================
    site = Site(domain="localhost:8000", name="localhost")
    user_info = {'email': 'Nicolas_cage@example.com', 
                 'first_name': 'Nick', 
                 'last_name': 'Cage', 
                 'password': 'admin', 
                 'skill_level':'5', 
                 'gender':'M', 
                 'nickname':'CageLover',
                 'site': site,
                 'url': 'open35'}
    #============================================================================
    
    
    
    def setUp(self):
            
        #=======================================================================
        # From userregistration.test
        #=======================================================================
        CustomUser.objects.create_inactive_user(**self.user_info)   
    
        #=======================================================================
        
        #=======================================================================
        # This is copied from execution.test, be carefull when touching this. 
        #=======================================================================
        Link.objects.create(text = "linkText", url = "Test", contestUrl = True, separator = False)
        
        Contest.objects.create(title = "TestContest", 
                               start_date = datetime.datetime(2034, 12, 12),
                               end_date = datetime.datetime(2036, 12, 12),
                               publish_date = datetime.datetime(2034, 12, 12),
                               teamreg_end_date = datetime.datetime(2034, 12, 12),
                               )
        
    
        c = Contest.objects.get(title = "TestContest") 
        c.links.add(Link.objects.get(text = "linkText"))
        
        
        Problem.objects.create(title = "TPS", description = self.set_problem_text(), 
                               date_uploaded = datetime.datetime(2035, 12, 12, 12, 30, 45),
                               contest = c)
        
        #=======================================================================
        
        
        
        
        #=======================================================================
        # Creating team 
        #=======================================================================
        Team.objects.create(name = "TestTeamSubmission", 
                            onsite = True, 
                            #members = CustomUser.objects.get(email = 'Nicolas_cage@example.com'),
                            contest = c
                            )
        
        #=======================================================================

        CompilerProfile.objects.create(name = "Java",
                                       compile = "cnc",
                                       package_name = "randomPakke",
                                       run = "rc"
                                       )
        
        Submission.objects.create(submission = 'media/submissions/DoNotDelete.pdf', 
                                  text_feedback = self.set_text_feedback(),
                                  team = Team.objects.get(name = "TestTeamSubmission"),
                                  problem = Problem.objects.get(title = "TPS"),
                                  compileProfile = CompilerProfile.objects.get(name = "java") 
                                  )        

    
    def test_submission_model_basic(self):
        s = Submission.objects.get(submission = 'media/submissions/DoNotDelete.pdf')

        self.assertEqual(s.submission, 'media/submissions/DoNotDelete.pdf', "Wrong filepath/name")
        self.assertEqual(s.team, Team.objects.get(name = "TestTeamSubmission"))
        self.assertEqual(s.text_feedback, self.set_text_feedback(), "Text feedback is not correct")
        self.assertEqual(s.problem, Problem.objects.get(title = "TPS"), "Problem is wrong")
        
        self.assertFalse(s.runtime, "Runtime is set wrong")        
        self.assertFalse(s.solved_problem, "Solved_problem should be false by default")
        
    
    def test_form(self):
        
        '''
        NOT working, sorry, dont know how to test this
        myfile = open('private\submissions\DoNotDelete.pdf','r')
        response = self.client.post('/', {'file':myfile}) 
        
        form_data = {'submission' : Submission.objects.get(submission = 'media/submissions/DoNotDelete.pdf').submission,
             'request.FILES': response}
        form = SubmissionForm(data = form_data)
        self.assertEqual(form.is_valid(), True, "Submission form is not valid")
        '''
        
        form_data = {'submission' : None}
        form = SubmissionForm(data = form_data)
        self.assertEqual(form.is_valid(), False, "Submission form should not be validated when nothing is sendt")
            
    
    def set_text_feedback(self):
        return "I am not a demon. I am a lizard,"
    
    def set_problem_text(self): 
        return "Passion is very important to me. If you stop enjoying things, you've got to look at it, because it can lead to all kinds of depressing scenarios."