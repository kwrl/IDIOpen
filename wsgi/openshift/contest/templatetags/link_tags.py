'''
Created on Feb 12, 2014

@author: filip
'''
from django import template
import os

register = template.Library()

@register.inclusion_tag('navigation.html')
def navigation(contest):
    links = contest.links
    return {'links': links,
            'contest': contest,}
    
@register.filter
def filename(value):
    return os.path.basename(value.file.name)
    