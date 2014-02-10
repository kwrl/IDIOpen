from django.test import TestCase
from openshift.Contest.models import Contest
from datetime import datetime


# Create your tests here.
class ContestTestCase(TestCase):
    def setUp(self):
        dateTime = datetime.now()
        Contest.objects.create(name="open2014", date=dateTime)
