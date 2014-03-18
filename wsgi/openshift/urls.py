from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from contest import views
from filebrowser.sites import site
from django.contrib.auth import views as auth_views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    (r'^grappelli/', include('grappelli.urls')),
    (r'^admin/filebrowser/', include(site.urls)),
    url(r'^login/$',
                           auth_views.login,
                           {'template_name': 'registration/bare_login.html'},
                           name='auth_login'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^password/change/$',
        auth_views.password_change,
        name='password_change'),
    url(r'^password/change/done/$',
        auth_views.password_change_done,
        name='password_change_done'),
    (r'^([^/]+)/', include('contest.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
