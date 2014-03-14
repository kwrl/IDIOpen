from django.contrib import admin
from contest.models import Contest, Link, Team, Invite
from django.contrib.auth import get_user_model

User = get_user_model()

class TeamAdmin(admin.ModelAdmin):
    filter_horizontal = ('members',)
    '''
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'members':
            kwargs["queryset"] = User.objects.all().exclude(members__in=Team.objects.all())
        return super(TeamAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
    '''


admin.site.register(Contest)
admin.site.register(Link)
admin.site.register(Team, TeamAdmin)
admin.site.register(Invite)


