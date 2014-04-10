from django.contrib import admin
from django import forms
from .models import Contest, Link, Team, Invite, ContactInformation, Sponsor
from .forms import LinkForm
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
            'fields': ('text', 'contestUrl', 'url','separator'),
            'description': "To create a separator, create a Link with url \'separator\' without slashes."
        }),
    )
    list_display = ('text', 'contestUrl', 'url',)
    search_fields = ('text','url',)
    ordering = ('text',)
    form = LinkForm

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



