#coding: utf-8
"""
Render tex/pdf/CSV for end users
"""
# Some latex is sensitive to newlines, beware

from django.shortcuts import render
from django.http import HttpResponse

import MySQLdb as mdb
from collections import defaultdict
from subprocess import Popen
from shlex import split
from os import path, makedirs, remove, listdir
import re, string
import csv
from zipfile import ZipFile
from StringIO import StringIO
from shutil import rmtree
from string import Template
from decimal import Decimal

from openshift.helpFunctions.views import get_most_plausible_contest
from openshift.contest.models import Team, Contest

SQL_FETCH_USERNAME_TEAM = \
"""
SELECT T.name, U.email
FROM contest_team AS T , userregistration_customuser AS U, contest_team_members AS CTM
WHERE CTM.team_id = T.id AND U.id = CTM.customuser_id AND T.onsite = 1
ORDER BY T.id
;
"""
FILENAME = "/tmp/outfile.csv"

TEAM_PARSELINE = "TEAM".decode('utf-8')
SPONSOR = "SPONSOR".decode('utf-8')
CON1 = "CONTESTANT1".decode('utf-8')
CON2 = "CONTESTANT2".decode('utf-8')
CON3 = "CONTESTANT3".decode('utf-8')
CONTEST_LOGO = "CONTEST_LOGO".decode('utf-8')
DEFAULT_EMPTY = r"""\ """.decode('utf-8')

SPONSOR_LATEX_PREAMBLE = r"""
\usepackage{caption, subfig}
\usepackage{graphicx}
\captionsetup[subfloat]{labelformat=empty}
\captionsetup[figure]{labelformat=empty}
""".decode('utf-8')

SPONSOR_IMAGE_LATEX = r"""
\subfloat[///SPONSORLABEL]{
\begin{tabular}{c}
\includegraphics[width=///PERCENTWIDTH \textwidth, height=2cm]{///SPONSOR_IMAGE_FILENAME}
\end{tabular}}""".decode('utf-8')

SPONSOR_IMAGE_PREFIX= r"""
\begin{figure}[ht]
 \caption[]{\textbf{Sponsors}}
""".decode('utf-8')

SPONSOR_IMAGE_SUFFIX = r"""\end{figure}""".decode('utf-8')

DIR_DEST = "/tmp/teams/".decode('utf-8')

class LatexTemplate(Template):
    delimiter = '///'

def render_semicolonlist(team_list):
    retString = ""
    team_contestant_dict = get_team_contestant_dict(team_list)
    for _, contestants in team_contestant_dict.iteritems():
        for c in contestants:
            retString += c + ";"

    return retString

def get_sponsor(contest):
    imageString = ""
    sponsors = contest.sponsors.all()
    if sponsors.count() < 1:
        return DEFAULT_EMPTY, {}
    imageWidth = str(Decimal(1) / Decimal(sponsors.count()))

    retDict = {}
    for index, spon in enumerate(sponsors):
        parse_string = LatexTemplate(SPONSOR_IMAGE_LATEX)
        d = {
            'SPONSOR_IMAGE_FILENAME': spon.image.path_full,
            'SPONSORLABEL' : spon.name,
            'PERCENTWIDTH': imageWidth[:3], # precision 3
        }
        retDict['SPONSOR%d_IMAGE_FILENAME' % (index + 1)] = spon.image.path_full
        imageString += parse_string.substitute(d)

    retString = SPONSOR_IMAGE_PREFIX + imageString + SPONSOR_IMAGE_SUFFIX
    return retString, retDict

def filter_team_name(team_name):
    pattern = re.compile(r'[\W_]+')
    return pattern.sub('', team_name)

def tex_render_unsafe(unsafe_string):
    retString = r"""\verb|""" . decode('utf-8') \
              + unsafe_string . replace("|", "") \
              + r"""|"""      . decode('utf-8')
    return retString

def add_preamble(latex_str):
    latex_str = latex_str.split('\n')
    latex_str.insert(1, SPONSOR_LATEX_PREAMBLE)
    return "\n".join(latex_str)

def cleanup_previous():
    if path.exists(DIR_DEST):
        rmtree(DIR_DEST)
    makedirs(DIR_DEST)

def populateContestants(con_list):
    con_dict = {}
    index = 1
    for con in con_list[:-1]:
        key = "CONTESTANT" + str(index)
        con_dict[key] = tex_render_unsafe(con) + ", "
        index += 1

    key = "CONTESTANT" + str(index)
    con_dict[key] = tex_render_unsafe(con_list[-1])

    return con_dict

def get_latex_init_dict(contest, team_name, contestants):
    logo = DEFAULT_EMPTY
    if contest.logo and len(contest.logo) > 0:
        logo = contest.logo.path_full

    #TODO: hardcoded logo is baaaaad practise

    ret = {
            TEAM_PARSELINE : tex_render_unsafe(team_name),
            SPONSOR: DEFAULT_EMPTY,
            CON1: DEFAULT_EMPTY,
            CON2: DEFAULT_EMPTY,
            CON3: DEFAULT_EMPTY,
            # CONTEST_LOGO: logo,
            CONTEST_LOGO: '/webapps/idi_open/wsgi/media/uploads/IDIOpen_logo.jpg',
            #CONTEST_LOGO: '/tmp/test.jpg',
            #.. to create empty image: convert -size 1x1 "xc:#FF0000" /tmp/test.jpg
            # requires imagemagick from repo
        }
    ret.update(populateContestants(contestants))
    return ret

def genOnePdf(pdf_files):
    string = ""
    for pdf in pdf_files:
        string += path.join(DIR_DEST, "%s " % (pdf ))

    output_pdf = path.join(DIR_DEST, "out.pdf")

    if len(pdf_files) == 1:
        output_pdf = string[:-1] # pop excess space
    else:
        proc=Popen(split('pdfunite %s %s' % (string, output_pdf)))
        proc.communicate()

    response = None
    response = HttpResponse(open(output_pdf), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="team.pdf"'

    return response

def genManyPdf(pdf_files):
    s = StringIO()
    zf = ZipFile(s, mode='w')
    zf.filename = "teampdf.zip"

    for pdf in pdf_files:
        zf.write(path.join(DIR_DEST, pdf), arcname="teamPDF/" + pdf)
    zf.close()


    # Grab ZIP file from in-memory, make response with correct MIME-type
    response = HttpResponse(s.getvalue(), mimetype = "application/x-zip-compressed")
    # ..and correct content-disposition
    response['Content-Disposition'] = 'attachment; filename=%s' % zf.filename

    return response

def write_team_pdf(team_name, index, tex_dict, parser):
    file_name = DIR_DEST + filter_team_name(team_name) +  str(index) + '.tex'

    with open(file_name,'w') as f:
        write_buf = parser.substitute(tex_dict).encode('utf-8')
        f.write(write_buf)

    cmd_latex = "xelatex -no-file-line-error -halt-on-error" \
                + " -interaction=nonstopmode --output-directory="
    cmd_run= '%s"%s" %s' % (cmd_latex, DIR_DEST, file_name)

    proc=Popen(split(cmd_run))
    proc.communicate()

def process_team_contestants(latex_parse_string,
                            team_list, output_format, contest):
    cleanup_previous() # delete old tmp folder, create a new

    team_contestant_dict = get_team_contestant_dict(team_list)

    for index, tup in enumerate(team_contestant_dict.iteritems()):
        team_name, contestants = tup[0], tup[1]
        tex_dict = get_latex_init_dict(contest, team_name, contestants)
        #TODO: remove hardcode
        sponsor, sponsDict = get_sponsor(contest)
        tex_dict.update(sponsDict)
        if latex_parse_string.find("///SPONSOR ") > 0:
            latex_parse_string = add_preamble(latex_parse_string)
            tex_dict.update({SPONSOR: sponsor})

        parser = LatexTemplate(latex_parse_string)
        write_team_pdf(team_name, index, tex_dict, parser)

    pdf_files = [file for file in listdir(DIR_DEST) if file.endswith(".pdf")]

    if output_format == "teamCSV_onePDF":
        return genOnePdf(pdf_files)

    else:
        return genManyPdf(pdf_files)

# TODO: rewrite as ORM, this is sill
def get_contestant_println(con_obj):
    nickname = ''
    if con_obj.nickname:
        nickname = ' `' + con_obj.nickname + '` '
    return (con_obj.first_name + nickname + con_obj.last_name)

def get_team_contestant_dict(teams):
    team_members_dict = defaultdict( list )
    for team_id in teams:
        team = Team.objects.get(pk=int(team_id))
        teamname = team.name
        #team_members_dict[teamname].append(get_contestant_println(team.leader))
        for member in team.members.all():
            team_members_dict[teamname].append(get_contestant_println(member))
    return team_members_dict

# TODO: rewrite as ORM, this is silly
#FIXME: per default rendered to libreoffice, which cannot see the unicode?
def extract_to_csv():
    pass

def render_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    extract_to_csv()

    response = HttpResponse("<h1> Hello </h1>")
    with open(FILENAME, 'r') as f:
        response = HttpResponse(f.read(), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="csv_out.csv"'

    return response

def latex_view(request, contest_pk=None):
    contest = get_most_plausible_contest(contest_pk)
    if not contest:
        return HttpResponse("<h1> No contest </h1>")
    teams = Team.objects.filter(contest=contest, onsite='True')
    context = {
            'teams' : teams,
            'contests': Contest.objects.all(),
            'contest': contest,
            }

    return render(request, 'latex_home.html', context)

# EOF
