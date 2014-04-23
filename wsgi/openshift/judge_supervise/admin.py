""" Render the views for judges
"""
from django.contrib import admin
from django.db import models
from .models import judge_view

from .urls import get_urls

class judge_view_admin(admin.ModelAdmin):
    # FIXME
    """ Temporary solution to get a view connected in admin site
    """
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request):
        return False

        
    def get_urls(self):
        return get_urls(self, judge_view_admin)


admin.site.register(judge_view, judge_view_admin)

# EOF
