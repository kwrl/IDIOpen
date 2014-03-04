'''
Created on Feb 12, 2014

@author: filip
'''
from django.conf.urls import patterns, include, url
from contest import views
from article import views as articleview

# Into these URL's, the name of the contest is passed as a prefix to all 
# patterns below.

urlpatterns = patterns('',
    url(r'^$', views.index, name='home'), # Default
    (r'^accounts/', include('userregistration.urls')),
    # url(r'^blog/', include('blog.urls
    url(r'^article/(?P<article_id>\d+)/$', articleview.detail, name='detail'),
    url(r'^article/list/$', articleview.index, kwargs='contestURL', name='articleList'),
)
