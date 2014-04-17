from django.conf.urls import patterns, include, url
from .views import submission_view, submission_problem, highscore_view
from clarification.views import clarification

urlpatterns = patterns('',
    url(r'^$', submission_view, name = 'submission_page'),
    url(r'(?P<problemID>[\d]+)', submission_problem),
    url(r'highscore', highscore_view),
    url(r'clarification', clarification),
)

# EOF