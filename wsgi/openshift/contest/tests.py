#coding:utf8
from django.test import TestCase, Client
from userregistration.forms import RegistrationForm
from contest.forms import * 

# Create your tests here.
'''
This tests redirects
'''
class ContestURLTestCase(TestCase):
    fixtures = ['contest_testdata.json', 'contest_testdata']
    
    def setUp(self):
        pass
    
    def test_index(self):
        #Index
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('contests' in resp.context)        
                
    def test_contest_url(self):   
        resp = self.client.get('/open14/')
        self.assertEqual(resp.status_code, 200)

        # Ensure that non-existent contests throw a 404        
        resp = self.client.get('/open15/')
        self.assertEqual(resp.status_code, 404)


    def test_contest_register_url(self):
        resp = self.client.get('/open14/accounts/register/')
        self.assertEqual(resp.status_code, 200)
        
        # No input
        resp = self.client.post('/open14/accounts/register/')
        self.assertEqual(resp.status_code, 200)
            
    def test_contest_redirects_url(self):    
        # If not logged in, 301: Moved permantly?
        resp = self.client.get('/open14/team', follow=True)
        self.assertRedirects(resp, '/open14/accounts/login/', 301, 200, host=None, msg_prefix='')
        
        resp = self.client.get('open14/team/register/', follow=True)
        # What happens next?


'''
Tests the forms
'''
class ContestFormTestCase(TestCase):
    fixtures = ['contest_testdata.json', 'contest_testdata']
    
    def setUp(self):
        pass

    def test_loginUser_Form(self):
    #=======================================================================
    # Login from frontpage for competition
    # Check that you are successful with valid login information
    #=======================================================================
        c = Client()
        resp = c.post('/open14/', {'username' : 'nic@gmail.com', 'password' : 'kim123'})
        self.assertEqual(resp.status_code, 200)
        
        # TODO: Doesn't work atm? You get redirected (302), does that mean we don't get logged in?
        #resp = c.get('/open14/accounts/profile/')
        #self.assertEqual(resp.status_code, 200)
      
        # TODO: Need to test Logout better  
        #resp = c.logout()
        #self.assertEqual(resp.status_code, 200)
       
    def test_registerUser_Form(self):
        registerURL = "/open14/accounts/register/"
        # TODO: Testing the login Form
        #Empty input in all fields
        response = self.client.post(registerURL, {'':''})
        self.assertFormError(response, 'form', 'email', 'This field is required.')
        
        #Invalid E-mail
        response = self.client.post(registerURL, {'email':'invalid_email@'})
        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')

    def test_registerUser_invalid_form(self):
        data = {'email' : '}{±±±'}        
        form = RegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        

        # Skill_level and Gender with values not included in the choiceField
        data = {'email' : 'TheCage@hotmail.com', 'first_name' : 'Nicolas', 'last_name' : 'Cage', 
                'password1' : 'kim123', 'password2' : 'kim123', 'skill_level' : 'Pro', 
                'gender' : '\'); Drop table teams;--'}
        form = RegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        
        data = {'email' : 'TheCage@hotmail.com', 'first_name' : 'Nicolas', 'last_name' : 'Cage', 
                'password1' : 'kim123', 'password2' : 'kim123', 'skill_level' : 'invalidInput', 
                'gender' : 'M'}
        form = RegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        
        # First name with only spaces
        data = {'email' : 'TheCage@hotmail.com', 'first_name' : '     ', 'last_name' : 'Cage', 
                'password1' : 'kim123', 'password2' : 'kim123', 'skill_level' : 'Pro', 
                'gender' : 'M'}
        form = RegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        
        # Last name with only spaces
        data = {'email' : 'TheCage@hotmail.com', 'first_name' : 'Nicolas', 'last_name' : '       ', 
                'password1' : 'kim123', 'password2' : 'kim123', 'skill_level' : 'Pro', 
                'gender' : 'M'}
        form = RegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        
        # Password1 != Password2
        data = {'email' : 'TheCage@hotmail.com', 'first_name' : 'Nicolas', 'last_name' : '       ', 
                'password1' : 'nic123', 'password2' : 'kim123', 'skill_level' : 'Pro', 
                'gender' : 'M'}
        form = RegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        
            
    def test_registerUser_valid_form(self):
        data = {'email' : 'TheCage@hotmail.com', 'first_name' : 'Nicolas', 'last_name' : 'Cage', 
                'password1' : 'kim123', 'password2' : 'kim123', 'skill_level' : 'Pro', 'gender' : 'M'}
        form = RegistrationForm(data=data)
        self.assertTrue(form.is_valid())
        
        
    
    
    def test_create_simple_team_onsite_valid_form(self):
        '''
        First test for the simplest case
        '''
        '''
        data = {'name' : 'TestTeamName', 'onsite':'True'}
        form = Team_Form(data=data)    
        self.assertTrue(form.is_valid())
        '''
        '''
        #test for spaces in team name
        data = { 'name' : 'Test TeamName', 'onsite':'True'}
        form = Team_Form(data=data)    
        self.assertTrue(form.is_valid())
        '''
        
        #testing for spaces AFTER team name, should no be legal
        data = { 'name' : 'Test TeamName        ', 'onsite':'True'}
        form = Team_Form(data=data)
        self.assertEqual(form.clean_name(), 'Test TeamName')
        
    
    def test_create_simple_team_onsite_invalid_form(self):
        #Test for names onsite false without setting offsite
        data = { 'name' : 'GentleCoding', 'onsite':'False'}
        form = Team_Form(data=data)    
        self.assertFalse(form.is_valid())
    
        
        #-----------------Spaces--------------------------------
        #test for only space in team name
        data = { 'name' : '  ', 'onsite':'True'}
        form = Team_Form(data=data)    
        self.assertFalse(form.is_valid())
        
        #test for only space
        data = { 'name' : '  ', 'onsite':'False'}
        form = Team_Form(data=data)    
        self.assertFalse(form.is_valid())

        
    '''
    Here start simple testing for UPDATEteam registration 
    '''
        
    def test_update_simple_team_valid_form(self):
        data = { 'name' : 'GentleCoding', 'onsite' : 'True'}
        form = Team_Edit(data=data)
        self.assertTrue(form.is_valid())
        
        #test for spaces in team name
        data = { 'name' : 'Test TeamName', 'onsite':'True'}
        form = Team_Edit(data=data)    
        self.assertTrue(form.is_valid())
        
        #testing for spaces AFTER team name, should no be legal
        data = { 'name' : 'Test TeamName        ', 'onsite':'True'}
        form = Team_Edit(data=data)
        self.assertEqual(form.clean_name(), 'Test TeamName')
        
        data = { 'name' : 'Test TeamName        ', 'onsite':'False','ofsite':'Bergen'}
        form = Team_Edit(data=data)
        self.assertTrue(form.clean())
        
        #empty offsite
        data = { 'name' : 'Test TeamName', 'onsite':'False','ofsite':''}
        form = Team_Edit(data=data)
        self.assertTrue(form.clean())
        
        data = { 'name' : 'Test TeamName', 'onsite':'False','ofsite':'  '}
        form = Team_Edit(data=data)
        self.assertTrue(form.clean())
        
        
        
    def test_update_simple_team_invalid_form(self):
        #Testing that you need to speicify ofsite
        data = { 'name':'GentleCoding', 'onsite':'False'}
        form = Team_Edit(data=data)
        self.assertFalse(form.IsValid())
        
        data = { 'name':'', 'onsite':'True'}
        form = Team_Edit(data=data)
        self.assertFalse(form.IsValid())
        
        data = { 'name':' ', 'onsite':'True'}
        form = Team_Edit(data=data)
        self.assertFalse(form.IsValid())
        
    
