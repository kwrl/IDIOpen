from django.contrib import admin
from contest.models import Sponsor #weird error..Haakon 
from django import forms
from contest.models import Contest, Link, Team, Invite, ContactInformation

from django.contrib.auth import get_user_model

User = get_user_model()

class TeamForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)
        self.fields['members'].queryset = User.objects.all().exclude(
                members__in=Team.objects.filter(contest = self.instance.contest).exclude(
                id=self.instance.id)).exclude(is_staff=True)
        
class TeamAdmin(admin.ModelAdmin):
    filter_horizontal = ('members',)
    
    form = TeamForm
    
    
class LinkAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('text', 'contestUrl', 'url'),
            'description': "Collections of links can be separated into several blocks by adding a separator block. Simply type 'SEPARATOR' in the url field to make a separator."
        }),
    )
    list_display = ('text', 'contestUrl', 'url',)
    search_fields = ('text','url',)
    ordering = ('text',)
    
class ContestAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'start_date','end_date','publish_date')
    search_fields = ('title', 'url',)
    ordering = ('title',)
    
class InviteAdmin(admin.ModelAdmin):
    list_display = ('email', 'team',)
    search_fields = ('email', 'team',)
    ordering = ('email',)
    
class SponsorAdmin(admin.ModelAdmin):
    list_display = ('name', 'url',)
    search_fields = ('name', 'url',)
    ordering = ('name',)

admin.site.register(Contest, ContestAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(Invite, InviteAdmin)
admin.site.register(ContactInformation)



