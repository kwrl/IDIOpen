from django.conf.urls import patterns, include, url

import openshift.node_manage.views

urlpatterns = patterns('',
        url('^a$', openshift.node_manage.views.index, name='test'),
    )

# EOF
