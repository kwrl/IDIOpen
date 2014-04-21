""" Render the views for judges
"""

from django.contrib import admin

from .urls import get_urls

class judge_view_admin(admin.ModelAdmin):
    # FIXME
    """ Temporary solution to get a view connected in admin site
    """
    view_on_site = True
    class Media:
        """ https://docs.djangoproject.com/en/1.6/ref/contrib/
            admin/#django.contrib.admin.ModelAdmin.get_urls
        """

    def get_urls(self):
        return get_urls(self, judge_view_admin)

class string_with_title(str):
    def __new__(cls, value, title):
        instance = str.__new__(cls, value)
        #pylint:disable=W0212
        instance._title = title
        return instance

    def title(self):
        return self._title

    __copy__ = lambda self: self
    __deepcopy__ = lambda self, memodict: self

from django.db import models
class judge_view(models.Model):
    class Meta:
        app_label = string_with_title("Judge_Supervisor", "Judge_Supervisor")

        managed = False # prevent from entering the DB
        verbose_name = "Click here to supervise"
        verbose_name_plural = "Click here to supervise"

admin.site.register(judge_view, judge_view_admin)

# EOF

