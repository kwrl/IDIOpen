'''
Created on Feb 26, 2014

@author: filip
'''
from django.dispatch import Signal

# A user has been edited
#user_edited = Signal(providing_args=["user", "request"])

# A new user has registered.
user_registered = Signal(providing_args=["user", "request"])

# A user has activated his or her account.
user_activated = Signal(providing_args=["user", "request"])