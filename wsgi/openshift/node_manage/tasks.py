from __future__ import absolute_import

from djcelery import celery

from openshift.messaging import celery_app as app

@app.task
def add(x, y):
    return x + y
