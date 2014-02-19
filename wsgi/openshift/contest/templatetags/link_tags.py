'''
Created on Feb 12, 2014

@author: filip
'''
from django import template
from openshift.contest.models import Contest
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
import os

register = template.Library()

@register.inclusion_tag('navigation.html')
def navigation(contest):
    links = contest.links
    return {'links': links,
            'contest': contest,}

@register.assignment_tag(takes_context=True)
def contest(context):
    request = context['request']
    url = request.path.split('/')[1]
    try:
        contest = Contest.objects.get(url=url)
    except ObjectDoesNotExist:
        raise Http404
    return contest
    
@register.filter
def filename(value):
    return os.path.basename(value.file.name)
    