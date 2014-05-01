""" to be used in the (modeladmin) view class
"""
from django.conf.urls import url, patterns
from django.contrib import admin

from .views import  render_csv, latex_view



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
    #import ipdb; ipdb.set_trace()
    my_urls = patterns('',
        url(r'^con(?P<contest_pk>[0-9]+)$',
            admin.site.admin_view(inst.changelist_view)),
         )
    return my_urls + urls

# EO dsdsF

