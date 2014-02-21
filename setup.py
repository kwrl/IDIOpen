from setuptools import setup

import os

# Put here required packages
packages = ['Django<=1.6','django-grappelli','django-filebrowser','django-registration', 'south',]

if 'REDISCLOUD_URL' in os.environ and 'REDISCLOUD_PORT' in os.environ and 'REDISCLOUD_PASSWORD' in os.environ:
     packages.append('django-redis-cache')
     packages.append('hiredis')


setup(name='GentleIDI',
      version='1.0',
      description='OpenShift App',
      author='GentleCoding',
      author_email='example@example.com',
      url='https://pypi.python.org/pypi',
      install_requires=packages,
)

