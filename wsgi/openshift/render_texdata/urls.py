""" to be used in the (modeladmin) view class -
    the urls used here are special in that they override default
    admin URLS (from modeladmin). This is to enable simple access from the
    django admin interface
"""
from django.conf.urls import url, patterns
from django.contrib import admin

from .views import  render_csv

def render_csv_url(inst, class_super):
    urls = super(class_super, inst).get_urls()
    urls = [urls[0], ]
    #urls = []
    my_urls = patterns('',
       url(r'^$',
                admin.site.admin_view(render_csv,
                                      cacheable=True)),
       url(r'^(?P<contest_pk>[0-9]+)$',
                admin.site.admin_view(render_csv)),
    )

    return my_urls + urls

def latex_url(inst, class_super):
    urls = super(class_super, inst).get_urls()
    urls = [urls[0], ]
    my_urls = patterns('',
        url(r'^con(?P<contest_pk>[0-9]+)$',
            admin.site.admin_view(inst.changelist_view)),
         )
    return my_urls + urls

# EOF
