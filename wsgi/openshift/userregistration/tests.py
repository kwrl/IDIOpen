from django.test import TestCase, Client
from userregistration.models import CustomUser
from django.contrib.sites.models import Site
from django.core import mail
# Create your tests here.
class UserTestCase(TestCase):
    
    site = Site(domain="localhost:8000", name="localhost")
    user_info = {'email': 'filip.egge@gmail.com', 
                 'first_name': 'Filip', 
                 'last_name': 'Egge', 
                 'password': 'admin', 
                 'skill_level':'4', 
                 'gender':'M', 
                 'nickname':'Filip0',
                 'site': site,
                 'url': 'open14'}
    def setUp(self):
        CustomUser.objects.create_inactive_user(**self.user_info)
        
    def testUser(self):
        user = CustomUser.objects.get(email='filip.egge@gmail.com')
        self.failIf(user.is_active)
        self.assertEqual(user.get_full_name(), 'Filip Egge')
        self.assertEqual(user.get_name_nick(), 'Filip "Filip0" Egge')
        self.failUnless(user.check_password('admin'))
        
    def testActivation(self):
        user = CustomUser.objects.get(email='filip.egge@gmail.com')
        user2 = CustomUser.objects.activate_user(user.activation_key) 
        self.assertEqual(user, user2)
        
    def test_activation_email(self):
        mail.outbox = []
        user = CustomUser.objects.get(email='filip.egge@gmail.com')
        user.send_activation_email(self.user_info['site'], self.user_info['url'])
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.user_info['email']])
