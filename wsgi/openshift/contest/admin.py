from django.contrib import admin
from openshift.contest.models import Contest, Link, Team, Contestant
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from openshift.contest.models import CustomUser
from openshift.contest.forms import CustomUserChangeForm, CustomUserCreationForm
from django.db.models import Q

class Admin(CustomUser):
    class Meta:
        proxy = True
        app_label = 'auth'
        verbose_name = 'Admin account'
        verbose_name_plural = 'Admin accounts'

class Team(CustomUser):
    class Meta:
        proxy = True
        app_label = 'contest'
        verbose_name = 'Team User'
        verbose_name_plural = 'Team Users'


class TeamInline(admin.StackedInline):
    model = Team
    can_delete = False
    verbose_name_plural = 'Teams'
    filter_horizontal = ('members',)
    

class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference the removed 'username' field
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2')}
        ),
    )
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('email', 'name', 'is_staff',)
    search_fields = ('email', 'name',)
    ordering = ('email',)
    
    def queryset(self, request):
        qs = super(UserAdmin, self).queryset(request)
        qs = qs.filter(Q(is_staff=True) | Q(is_superuser=True))
        return qs
    
class CustomTeamAdmin(UserAdmin):
    # The forms to add and change user instances

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference the removed 'username' field
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2')}
        ),
    )
    inlines = (TeamInline, )
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('email', 'name', 'is_staff',)
    search_fields = ('email', 'name',)
    ordering = ('email',)
    
    def queryset(self, request):
        qs = super(UserAdmin, self).queryset(request)
        qs = qs.exclude(Q(is_staff=True) | Q(is_superuser=True))
        return qs

admin.site.register(Admin, CustomUserAdmin)
admin.site.register(CustomUser, CustomTeamAdmin)
admin.site.register(Contest)
admin.site.register(Link)
admin.site.register(Team)
admin.site.register(Contestant)