from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from contest import views
from filebrowser.sites import site
admin.autodiscover()



urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^admin/filebrowser/', include(site.urls)),
    (r'^accounts/', include('userregistration.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^([^/]+)/', include('contest.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
