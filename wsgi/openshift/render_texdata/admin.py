""" To be refactored
"""

from django.contrib import admin, messages
from django.contrib.admin import helpers
from django.contrib.admin.util import lookup_needs_distinct
from django.contrib.admin.views.main import ERROR_FLAG
from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse, render
from django.template.response import SimpleTemplateResponse
from django.utils.translation import ugettext as _
from django.utils.translation import ungettext
from django.utils.encoding import force_text

from functools import partial, reduce, update_wrapper
from glob import glob
import operator, re

from openshift.contest.models import Contest, Team
from openshift.helpFunctions.views import get_most_plausible_contest
from .models import RenderTexOrEmail
from .urls import render_csv_url, latex_url
from .views import process_team_contestants, render_semicolonlist, get_teamnames

class IncorrectLookupParameters(Exception):
    pass

def _doAction(request, selected, contest):
    if not selected or len(selected) < 1 or selected[0] == '':
        messages.error(request, "No team selected")
        return

    FORMAT_ERR = ["Invalid formatting, ensure all given variables are on" +
                    "the form ///VARIABLE",
                 "Error message: %s"
                 ]
    INVALID_VAR_ERR = ["No match for %s"]
    MISSING_PROG_ERR = ["Please verify that you have %s and %s installed" \
                        % ("xelatex", "pdfunite")]

    if "buttonId" in request.POST:
        if request.POST["buttonId"] == "emailCSV":
            try:
                # Response = email_view(selected)
                semicolon_list = render_semicolonlist(selected)
            except (KeyError,ValueError) as e:
                messages.error(request, str(e))

        elif request.POST["buttonId"] == "teamCSV_onePDF" \
        or request.POST["buttonId"] == "teamCSV_manyPDF":
            try:
                response = process_team_contestants(
                        request.POST['text'], selected,
                        request.POST['buttonId'], contest)
                return response
            except ValueError as ve:
                messages.error(request, FORMAT_ERR[0])
                messages.error(request, FORMAT_ERR[1] % str(ve))
            except KeyError as ke:
                messages.error(request, INVALID_VAR_ERR % str(ke))
            except OSError:
                messages.error(request, MISSING_PROG_ERR)
            except IOError:
                logfile = glob('/tmp/teams/*.log')
                messages.error(request,
                        "xelatex failed to compile")
                for log in logfile:
                    latex_compile_stdout = ""
                    with open(log, 'r') as f:
                        for line in f:
                            latex_compile_stdout += line + '\n'
                            if line.startswith('!'):
                                messages.error(request, line)
        else:
            teamname_list = get_teamnames(selected)


def _getContest(request, contest_pk=None):
    contest = re.search(r'\d{1,3}$', request.path)
    if contest:
        contest = Contest.objects.get(pk=int(contest.group()))
    else:
        contest = get_most_plausible_contest(contest_pk)
    return contest

class LatexAdmin(admin.ModelAdmin):
    def get_urls(self):
        """ Override to get custom admin views from the admin site """
        return latex_url(self, LatexAdmin)

    def get_queryset(self, request):
        """
        Returns a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """
        # Future developers might want to find a better way to retreive the
        # contest here it is extracted from the URL
        contest = re.search(r'\d{1,3}$', request.path)
        if contest:
            contest = Contest.objects.get(pk=str(contest.group()))
        else:
            contest = get_most_plausible_contest(contest)
            if not contest:
                return HttpResponse("<h1> No contests in system </h1>")

        # Fetch contests and order them - earliest first
        qs = self.model._default_manager.filter(contest=contest)
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def get_search_results(self, request, queryset, search_term):
        """
        Returns a tuple for each team
        and a boolean indicating if the results may contain duplicates.
        """
        self.opts = Team._meta
        # Apply keyword searches.
        def construct_search(field_name):
            if field_name.startswith('^'):
                return "%s__istartswith" % field_name[1:]
            elif field_name.startswith('='):
                return "%s__iexact" % field_name[1:]
            elif field_name.startswith('@'):
                return "%s__search" % field_name[1:]
            else:
                return "%s__icontains" % field_name

        use_distinct = False
        if self.search_fields and search_term:
            orm_lookups = [construct_search(str(search_field))
                           for search_field in self.search_fields]
            for bit in search_term.split():
                or_queries = [models.Q(**{orm_lookup: bit})
                              for orm_lookup in orm_lookups]
                queryset = queryset.filter(reduce(operator.or_, or_queries))
            if not use_distinct:
                for search_spec in orm_lookups:
                    if lookup_needs_distinct(self.opts, search_spec):
                        use_distinct = True
                        break

        return queryset, use_distinct

    def changelist_view(self, request, extra_context=None, contest_pk=None):
        """
        The 'change list' admin view for this model.
        """
        contest = _getContest(request)
        if not contest:
            return HttpResponse("<h1> No contests in system </h1>")

        semicolon_list = None
        latex_compile_stdout = None
        teamname_list = None

        if request.method == "POST":
            _doAction(request, request.POST['teams'].split(','), contest,)

        self.model = Team
        opts = self.model._meta
        #app_label = opts.app_label

        # Render the queryset's view properties
        list_display = ('name', 'onsite', 'contest', 'leader', 'offsite',)
        list_display_links = self.get_list_display_links(request, list_display)
        list_filter = ('onsite', 'contest',)
        actions = self.get_actions(request)
        search_fields = ['id', 'name']

        list_display = ['action_checkbox'] + list(list_display)

        self.search_fields = search_fields
        ChangeList = self.get_changelist(request)
        cl = ChangeList
        try:
            cl = ChangeList(request, self.model, list_display,
                list_display_links, list_filter, self.date_hierarchy,
                self.search_fields, self.list_select_related,
                self.list_per_page, self.list_max_show_all, self.list_editable,
                self)
        except IncorrectLookupParameters:
            if ERROR_FLAG in request.GET.keys():
                return SimpleTemplateResponse('admin/invalid_setup.html', {
                    'title': _('Database error'),
                })
            return HttpResponseRedirect(request.path + '?' + ERROR_FLAG + '=1')

        selected = request.POST.getlist(helpers.ACTION_CHECKBOX_NAME)

        formset = cl.formset = None

        # Handle GET -- construct a formset for display.
        if cl.list_editable:
            FormSet = self.get_changelist_formset(request)
            formset = cl.formset = FormSet(queryset=cl.result_list)


        # Build the list of media to be used by the formset.
        if formset:
            media = self.media + formset.media
        else:
            media = self.media

        # Build the action form and populate it with available actions.
        if actions:
            action_form = self.action_form(auto_id=None)
            action_form.fields['action'].choices = \
                                    self.get_action_choices(request)
        else:
            action_form = None

        selection_note_all = ungettext('%(total_count)s selected',
            'All %(total_count)s selected', cl.result_count)


        context = {
            'module_name': force_text(opts.verbose_name_plural),
            'selection_note': _('0 of %(cnt)s selected')
                                % {'cnt': len(cl.result_list)},
            'selection_note_all': selection_note_all
                                    % {'total_count': cl.result_count},
            'selection_counter': selection_note_all
                                    % {'total_count': cl.result_count},
            'title': 'Select teams to render email-line or latex-rendition',
            'is_popup': cl.is_popup,
            'cl': cl,
            'media': media,
            'has_add_permission': self.has_add_permission(request),
            'opts': cl.opts,
            # 'app_label': app_label,
            'app_label': 'Render your information here',
            'action_form': action_form,
            # 'actions_on_top': self.actions_on_top,
            'actions_on_top': None,
            # 'actions_on_bottom': self.actions_on_bottom,
            'actions_on_bottom': None,
            'actions_selection_counter': self.actions_selection_counter,
            'preserved_filters': self.get_preserved_filters(request),
            'semicolon_list' : semicolon_list,
            'contests': Contest.objects.all(),
            'contest': contest,
            'latex_compile_stdout' : latex_compile_stdout,
            'teamname_list': teamname_list,
            }
        context.update(extra_context or {})

        return render(request, 'latex_home.html', context)

class RenderAdmin(admin.ModelAdmin):
    """ Dummy class to render the CSV-download link
    """
    def get_urls(self):
        return render_csv_url(self, RenderAdmin)

admin.site.register(RenderTexOrEmail, LatexAdmin)

#admin.site.register(RenderCSV, RenderAdmin)
#admin.site.register(RenderCSV)
