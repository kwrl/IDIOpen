'''
Created on Feb 12, 2014

@author: filip
'''
from django.conf.urls import patterns, include, url
from contest import views
from article import views as articleview

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.index, name='home'),
    (r'^accounts/', include('userregistration.urls')),
    # url(r'^blog/', include('blog.urls')),
    url(r'^article/(?P<article_id>\d+)/$', articleview.detail, name='detail'),
    url(r'^article/list/$', articleview.index, name='articleList'),
    url(r'^registration/$', views.registration, name = 'register_teams'),
    url(r'^registration/registrationComplete/$', views.registrationComplete, name = 'register_team_complete'),
)