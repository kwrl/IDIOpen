'''
Created on Feb 12, 2014

@author: filip
'''
from django.conf.urls import patterns, include, url
from contest import views
from article import views as articleview

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.index, name='contest_list'),
    (r'^accounts/', include('userregistration.urls')),
    # url(r'^blog/', include('blog.urls')),
    url(r'^article/(?P<article_id>\d+)/$', articleview.detail, name='article_detail'),
    url(r'^article/list/$', articleview.index, name='articleList'),
    url(r'^registration/$', views.registration, name = 'register_teams'),
    url(r'^registration/registrationComplete/$', views.registrationComplete, name = 'register_team_complete'),
    url(r'^team/$', views.team_profile, name = 'team_profile'),
    url(r'^team/edit/$', views.editTeam, name = 'team_edit'),
    url(r'^team/member/delete/(?P<member_id>\d+)/$', views.deleteMember, name = 'team_delete_member'),
    url(r'^pages/(?P<article_url>[^/]+)/$', articleview.detail_url, name='article_detail_url'),
    url(r'^viewteams/$', views.view_teams, name = 'view_teams'),
    url(r'^leaveteam$', views.leave_team, name = 'team_leave'),    
    
)
