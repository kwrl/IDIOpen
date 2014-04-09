
from django.test import TestCase

from .models import Problem
from openshift.contest.models import Contest, Link
import datetime

# Create your tests here.

class testExecutionModels(TestCase):
    def setUp(self):
        text = self.setText()
        
        Link.objects.create(text = "linkText", url = "Test", contestUrl = True, separator = False)
        
        Contest.objects.create(title = "TestContest", 
                               start_date = datetime.datetime(2034, 12, 12),
                               end_date = datetime.datetime(2036, 12, 12),
                               publish_date = datetime.datetime(2034, 12, 12),
                               teamreg_end_date = datetime.datetime(2034, 12, 12),
                               )
        
    
        c = Contest.objects.get(title = "TestContest") 
        c.links.add(Link.objects.get(text = "linkText"))
        
        
        Problem.objects.create(title = "TestProblem", description = self.setText(), 
                               date_uploaded = datetime.datetime(2035, 12, 12, 12, 30, 45),
                               contest = c)
        
        
    def test_problem_model(self):
        problem = Problem.objects.get(title = "TestProblem")
        self.assertEqual(problem.title, "TestProblem")
        self.assertEqual(problem.description, self.setText())
        self.assertEqual(problem.contest, Contest.objects.get(title = "TestContest"))
        pass
        
    def setText(self):
        return "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut aliquam dolor massa, sed accumsan diam accumsan in. Curabitur vel purus non lorem eleifend vehicula. Maecenas eu leo imperdiet, consequat ipsum in, euismod lorem. Mauris lobortis dolor vitae nisl rutrum posuere. Praesent at arcu leo. Nam id est ipsum. Proin vel lacinia eros, vitae lobortis urna. Morbi dapibus vel leo non adipiscing. Morbi at neque enim. Maecenas non eros justo.Proin lacinia pulvinar arcu ac facilisis. Vivamus ultrices diam blandit est commodo mollis. Cras volutpat mi laoreet orci mattis, rutrum tempor sapien dapibus. Nam metus nulla, fringilla quis libero ut, tristique fringilla augue. Curabitur posuere est vel quam gravida consectetur. Proin convallis lectus eget volutpat aliquam. Nunc nec vehicula neque.Duis non quam massa. Interdum et malesuada fames ac ante ipsum primis in faucibus. Nunc nibh urna, dignissim sit amet dictum ut, eleifend non neque. Nam at sodales sapien, ac bibendum risus. Vivamus varius metus in augue ultricies, sed scelerisque leo sodales. Fusce blandit nisi non sem luctus, non porttitor arcu egestas. Ut et felis a lectus euismod fermentum. Mauris eu dapibus sem, sed condimentum dolor. Duis odio enim, faucibus eu dictum at, vulputate eget sem. Integer lacinia, arcu vel dictum aliquam, magna dolor consequat tortor, vel bibendum orci leo vitae neque. Mauris eget elementum leo.Sed eu commodo lorem. Mauris vitae nunc in nunc pellentesque convallis. Ut vel sem quam. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Interdum et malesuada fames ac ante ipsum primis in faucibus. Donec tristique ut sem quis lobortis. Suspendisse volutpat arcu orci, nec egestas erat molestie sed.Curabitur turpis nisl, gravida a consequat ac, pellentesque id justo. Pellentesque egestas lacinia diam, at tempor nisi mattis in. Etiam a orci dolor. Cras eu convallis nulla. Aenean congue interdum euismod. Sed congue varius elit a interdum. Quisque ligula mauris, egestas in ullamcorper a, convallis a neque. Donec vel laoreet tellus. Integer eget risus dapibus, posuere ante id, sodales nisi. Praesent nec leo arcu. Ut quis augue risus. Praesent nibh justo, ornare at pulvinar eget, feugiat convallis nibh. Proin non mattis risus. Vivamus dictum justo libero, egestas varius purus egestas quis. Suspendisse ac purus nec turpis aliquet fringilla eu nec leo."
