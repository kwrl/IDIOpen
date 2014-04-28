from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from filebrowser.sites import site
from openshift.contest import views
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'openshift.views.home', name='home'),
    url(r'^test/$', 'openshift.views.taskTest'),
    # url(r'^blog/', include('blog.urls')),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^admin/filebrowser/', include(site.urls)),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'^login/$',
                           auth_views.login,
                           {'template_name': 'registration/bare_login.html'},
                           name='auth_login'),
    url(r'^admin/', include(admin.site.urls)),
    (r'^([^/]+)/', include('openshift.contest.urls')),
    url(r'^node/', include('openshift.node_manage.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
