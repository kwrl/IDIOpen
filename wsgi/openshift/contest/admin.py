from django.contrib import admin
from openshift.contest.models import Contest, Link, Team

admin.site.register(Contest)
admin.site.register(Link)
admin.site.register(Team)


