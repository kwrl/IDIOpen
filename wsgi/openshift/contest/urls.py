'''
Created on Feb 12, 2014

@author: filip
'''
from django.conf.urls import patterns, include, url
from openshift.contest import views
from openshift.article import views as articleview

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.index, name='contest_list'),
    url(r'^accounts/', include('openshift.userregistration.urls')),
    url(r'^submission/', include('openshift.teamsubmission.urls')),       
    url(r'^problem/', include('openshift.teamsubmission.urls')),       

    # url(r'^blog/', include('blog.urls')),
    url(r'^article/(?P<article_id>\d+)/$', articleview.detail, name='article_detail'),
    url(r'^article/list/$', articleview.index, name='articleList'),
    url(r'^team/register/$', views.registration, name = 'register_teams'),
    url(r'^team/register/complete/$', views.registrationComplete, name = 'register_team_complete'),
    url(r'^team/$', views.team_profile, name = 'team_profile'),
    url(r'^team/edit/$', views.editTeam, name = 'team_edit'),
    url(r'^team/member/delete/(?P<member_id>\d+)/$', views.deleteMember, name = 'team_delete_member'),
    url(r'^teams/$', views.view_teams, name = 'view_teams'),
    url(r'^team/leave/$', views.leave_team, name = 'team_leave'),
    url(r'^pages/(?P<article_url>[^/]+)/$', articleview.detail_url, name='article_detail_url'), 
    url(r'^cage$', views.cage_me, name = 'nic_cage'), 
)

# EOF
