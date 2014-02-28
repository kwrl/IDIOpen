'''
Created on Feb 12, 2014

@author: filip
'''
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from openshift.contest import views
from openshift.article import views as articleview

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.index, name='home'),
    (r'^accounts/', include('userregistration.urls')),
    # url(r'^blog/', include('blog.urls')),
    url(r'^article/(?P<article_id>\d+)/$', articleview.detail, name='detail'),
    url(r'^article/list/$', articleview.index, name='articleList'),
)