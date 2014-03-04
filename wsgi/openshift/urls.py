#coding:utf-8

from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.dates import DateDetailView;
       
from contest import views, models
from filebrowser.sites import site
admin.autodiscover()

# To capture a value from the URL, just put parenthesis around it.


urlpatterns = patterns('',
    # Examples:
    (r'^grappelli/', include('grappelli.urls')),

    (r'^admin/filebrowser/', include(site.urls)),

    url(r'^admin/', include(admin.site.urls)),

    # pass name of contest as suffix
    # url(r'^([^/]+)/', include('contest.urls')), 
    url(r'(?P<contestURL>[-\w]+)/', include('contest.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
