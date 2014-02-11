from openshift.contest import TestCase
from openshift.contest.models import Contest
from openshift.contest import datetime


# Create your tests here.
class ContestTestCase(TestCase):
    def setUp(self):
        dateTime = datetime.now()
        Contest.objects.create(title="IDI Open 2014")
