#pylint: disable=C0103, E1120, E0602
'''
Created on Feb 27, 2014

@author: filip
'''
from django.conf.urls import patterns
from django.conf.urls import url
from django.views.generic.base import TemplateView
from django.contrib.auth import views as auth_views;
from userregistration.views import *;
from userregistration.views import updateProfilePw;
from changeemail.views import ChangeEmailView;

urlpatterns = patterns('',
        url(r'^activate/complete/$',
            TemplateView.as_view(template_name=
                'registration/activation_complete.html'),
            name='registration_activation_complete'),
        # Activation keys get matched by \w+ instead of the more specific
        # [a-fA-F0-9]{40}; a bad activation key should still get to the view;
        # that way it can return a sensible "invalid key" message instead of a
        # confusing 404.
        url(r'^activate/(?P<activation_key>\w+)/$',
            ActivationView.as_view(),
            name='registration_activate'),
        
        # Writte by Haakon and Anders
        url(r'^profile/editEmail/(?P<activation_key>\w+)/$',
            ChangeEmailView.as_view(),
            name='registration_email'),
                       
        url(r'^register/$',
            RegistrationView.as_view(),
            name='registration_register'),
        url(r'^register/complete/$',
            TemplateView.as_view(template_name=
                'registration/registration_complete.html'),
            name='registration_complete'),
        url(r'^register/closed/$',
            TemplateView.as_view(template_name=
                'registration/registration_closed.html'),
            name='registration_disallowed'),
        url(r'^profile/$', user_profile, name='profile'),
        url(r'^profile/edit/password/$', updateProfilePw, name='profile_edit_password'),
        url(r'^profile/edit/email/', updateProfileEmail, name='profile_edit_email'),
        url(r'^profile/edit/info/$', updateProfilePI, name='profile_edit_info'),
        url(r'^profile/edit/$', user_profile, name='profile'),
        url(r'^login/$',
            auth_views.login,
            {'template_name': 'registration/login.html'},
            name='login'),
        url(r'^logout/$',
            auth_views.logout,
            {'template_name': 'registration/logout.html'},
            name='logout'),
        url(r'^password/reset/$',
            password_reset,
            name='password_reset'),
        url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
            password_reset_confirm,
            name='auth_password_reset_confirm'),
        url(r'^password/reset/complete/$',
            password_reset_complete,
            name='password_reset_complete'),
        url(r'^password/reset/done/$',
            password_reset_done,
            name='password_reset_done'),
        )
# EOF

