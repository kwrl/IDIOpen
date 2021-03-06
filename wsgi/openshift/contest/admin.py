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
                id=self.instance.id))
class TeamAdmin(admin.ModelAdmin):
    filter_horizontal = ('members',)
    list_display = ('name', 'contest', 'onsite', 'leader', 'offsite',)
    search_fields = ('name',)
    list_filter = ('onsite','contest')
    form = TeamForm

class LinkAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('text', 'contestUrl', 'url','separator'),
            'description': 'To create a separator, tick off the "Seperator" tickbox.'+
            ' If you want to create new page that only includes an article (e.g rules) write /page/[url] in url field. '
        }),
    )
    list_display = ('text', 'contestUrl', 'url',)
    search_fields = ('text','url',)
    ordering = ('text',)
    form = LinkForm

class ContestAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'start_date','end_date','publish_date')
    search_fields = ('title', 'url')
    ordering = ('title',)
class InviteAdmin(admin.ModelAdmin):
    list_display = ('email', 'team','is_member')
    search_fields = ('email', 'team')
    ordering = ('email',)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ('name', 'url',)
    search_fields = ('name', 'url',)
    ordering = ('name',)
    
class ContactInformationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    def get_contactInformation(self,obj):
        return obj
    search_fields = ('name', 'email',)
    ordering = ('name',)

admin.site.register(Contest, ContestAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(Invite, InviteAdmin)
admin.site.register(ContactInformation, ContactInformationAdmin)



