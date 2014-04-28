from django.contrib import admin
from django.shortcuts import HttpResponse

from openshift.contest.models import Team
from .models import Latex_Teamview, Latex_TeamText
from .urls import render_csv_url, latex_url

from openshift.helpFunctions.views import get_most_plausible_contest

class LatexAdmin(admin.ModelAdmin):
    def get_urls(self):
        return latex_url(self, LatexAdmin)

class RenderAdmin(admin.ModelAdmin):
    # FIXME
    """ Temporary solution to get a view connected in admin site
    """
    def get_urls(self):
        return render_csv_url(self, RenderAdmin)

admin.site.register(Latex_TeamText, LatexAdmin)

admin.site.register(Latex_Teamview, RenderAdmin)
#admin.site.register(Latex_Teamview)
