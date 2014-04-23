""" to be used in the (modeladmin) view class
"""
from django.conf.urls import url, patterns
from django.contrib import admin

from .views import judge_home, judge_submission_team, judge_team_summary

def get_urls(inst, class_super):
    urls = super(class_super, inst).get_urls()
    urls = [urls[0], ]
    my_urls = patterns('',
       url(r'^$',
                admin.site.admin_view(judge_home,
                                      cacheable=True)),
       url(r'^team(?P<team_pk>[0-9]+)' +
              '/problem(?P<problem_pk>[0-9]+)/$',
                admin.site.admin_view(judge_submission_team)),
       url(r'^team(?P<team_pk>[0-9]+)',
                admin.site.admin_view(judge_team_summary)),
       url(r'^con(?P<contest_pk>[0-9]+)$',
                admin.site.admin_view(judge_home)),
    )

    return my_urls + urls

# EOF
