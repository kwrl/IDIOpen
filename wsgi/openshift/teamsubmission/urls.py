from django.conf.urls import patterns, include, url
from .views import submission_view, submission_problem, highscore_view

urlpatterns = patterns('',
    url(r'^$', submission_view),
    url(r'(?P<problemID>[\d]+)', submission_problem),
    url(r'highscore', highscore_view),
)

# EOF