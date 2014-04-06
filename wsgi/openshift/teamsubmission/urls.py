from django.conf.urls import patterns, include, url
from .views import submission_view, submission_problem

urlpatterns = patterns('',
    url(r'^$', submission_view, name = 'submission_page'),
    url(r'(?P<problemID>[\d]+)', submission_problem),
)

# EOF