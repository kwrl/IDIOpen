"""
http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html#using-celery-with-django
"""

from __future__ import absolute_import
from celery import Celery
from django.conf import settings
import os

#from openshift import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'openshift.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messaging.settings')

app = Celery('messaging')
#app = Celery('tasks', backend='amqp',broker='amqp://guest@localhost:5672//')
# app.config_from_object(celeryconfig)
    # relative import from ${PWD} of invoking script
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

if __name__ == "__main__":
    app.start()
