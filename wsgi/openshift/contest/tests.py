from django.test import TestCase
from contest.models import Contest
from datetime import datetime


# Create your tests here.
class ContestTestCase(TestCase):
    def setUp(self):
        dateTime = datetime.now()
        Contest.objects.create(title="IDI Open 2014")
