#coding:utf-8

from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.dates import DateDetailView;
       
from contest import views, models
from filebrowser.sites import site
admin.autodiscover()

#
# To capture a value from the URL, just put parenthesis around it.


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls),),
    url(r'^grappelli/', include('grappelli.urls')),

    url(r'^admin/filebrowser/', include(site.urls)),
    #andesil @ filip : I'm deprecating this.
    # (r'^([^/]+)/', include('contest.urls')), 

    # Get the string-suffix from root, store it in contestURL,
    # pass it on to contest.urls
    # \w = any single word character
    url(r'(?P<contestURL>[-\w]+)/', include('contest.urls',app_name='contest')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# EOF
