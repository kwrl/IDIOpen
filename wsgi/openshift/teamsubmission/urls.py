from django.conf.urls import patterns, include, url
from .views import submission_view

urlpatterns = patterns('',
    url(r'^$', submission_view)
)

# EOF