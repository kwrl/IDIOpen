from django.shortcuts import render
from django.http import HttpResponse

import MySQLdb as mdb
from collections import defaultdict
from subprocess import Popen
from shlex import split
from os import path, makedirs, remove, walk, listdir
import re, string; 
import csv
from zipfile import ZipFile
from StringIO import StringIO
from shutil import rmtree

from openshift.helpFunctions.views import get_most_plausible_contest 
from openshift.contest.models import Team, Contest, Sponsor


SQL_FETCH_USERNAME_TEAM = \
"""
SELECT T.name, U.email 
FROM contest_team AS T , userregistration_customuser AS U, contest_team_members AS CTM 
WHERE CTM.team_id = T.id AND U.id = CTM.customuser_id AND T.onsite = 1
ORDER BY T.id
;
"""
FILENAME = "/tmp/outfile.csv"

#MYSQL_CON = mdb.connect('hv-6146.idi.ntnu.no', 'gentle', 'tacosushi', 'gentleidi', 3306);
#MYSQL_CON = mdb.connect('localhost', 'gentle', 'tacosushi', 'gentleidi', 3306);


CONTESTANT_PARSELINE = "%(contestant_line)s"
TEAM_PARSELINE = "%(team)s"
SPONSOR1 = "%(sponsor1)s"
SPONSOR2 = "%(sponsor2)s"
SPONSOR3 = "%(sponsor3)s"

PRIZE = "%(prize)s"

def render_semicolonlist(team_list):
    retString = ""
    team_contestant_dict = get_team_contestant_dict(team_list)
    for _, contestants in team_contestant_dict.iteritems():
        for c in contestants:
            retString += c + ";"

    return retString

def process_team_contestants(latex_parse_string, team_list, output_format, contest):
    team_contestant_dict = get_team_contestant_dict(team_list)
    # yesno = raw_input("This will make latex for each %s teams - are you sure?"
    #                  % (len(team_contestant_dict)) +  "(Y/N)\n" )
    # if yesno is not 'Y':
    #     return

    get_sponsor_logo_name(contest) # Returns list with sponsor objects
    dir_dest = "/tmp/teams/"
    if path.exists(dir_dest):
        rmtree(dir_dest)

    makedirs(dir_dest)

    pattern = re.compile('[\W_]+')

    sponsor_dict = {
            betweenParanthesis(SPONSOR1): ' ',
            betweenParanthesis(SPONSOR2): ' ',
            betweenParanthesis(SPONSOR3): ' ',
    }

    prize_dict = {
            betweenParanthesis(PRIZE): ' ',
        }

    for index, sponsor in enumerate(Sponsor.objects.all()):
        key = "sponsor" + str(index)
        sponsor_dict[key] = sponsor

    i = 0
    for team_name, contestants in team_contestant_dict.iteritems():
        tex_dict = {
               betweenParanthesis(CONTESTANT_PARSELINE) : renderingStr(contestants),
               betweenParanthesis(TEAM_PARSELINE)       : team_name}

        tex_dict.update(sponsor_dict)
        tex_dict.update(prize_dict)

        file_name = dir_dest + pattern.sub('', team_name) +  str(i) + '.tex'
    
        i += 1
        
        with open(file_name,'w') as f:
            try:
                string = latex_parse_string%tex_dict
            except ValueError:
                raise ValueError("Invalid format character! Format is \"\%(var)s\"")
            f.write(string.encode('utf-8'))

        proc=Popen(split('pdflatex -output-directory %s ' % (dir_dest) + file_name))
        proc.communicate()


    s = StringIO()
    #ZIP_FILE = "/tmp/teams.zip"
    zf = ZipFile(s, mode='w')
    zf.filename = "teampdf.zip"


    pdf_files = [file for file in listdir(dir_dest) if file.endswith(".pdf")]
    if len(pdf_files) == 1:
        file = path.join(dir_dest, pdf_files[0])
        response = HttpResponse(open(file), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="team.pdf"'
        return response

    if output_format == "teamCSV_onePDF":
        """ fuckup BEGING """
        string = ""
        for pdf in pdf_files:
            string += path.join(dir_dest, pdf + " ")

        monster_pdf = path.join(dir_dest, "out.pdf") 

        proc=Popen(split('pdfunite %s %s' % (string, monster_pdf)))
        proc.communicate()

        response = HttpResponse(open(monster_pdf), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="team.pdf"'

        return response

    else:
        for pdf in pdf_files:
            zf.write(path.join(dir_dest, pdf), arcname="teamPDF/" + pdf)
        zf.close()


        # Grab ZIP file from in-memory, make response with correct MIME-type
        response = HttpResponse(s.getvalue(), mimetype = "application/x-zip-compressed")
        # ..and correct content-disposition
        response['Content-Disposition'] = 'attachment; filename=%s' % zf.filename

        return response


def get_sponsor_logo_name(contest):
    contest_sponsor = Contest.objects.filter(title=contest.title).prefetch_related('sponsors')
    sponsor_list = []
    for contest in contest_sponsor:
        sponsors = contest.sponsors.all()
        for sponsor in sponsors:
            sponsor_list.append(sponsor)
    return sponsor_list    

def get_team_contestant_dict(teams):
    team_members_dict = defaultdict( list )
    for team_id in teams:
        team = Team.objects.get(pk=int(team_id))
        for member in team.members.all():
            team_members_dict[team.name].append(member.email)
    return team_members_dict


def renderingStr(contestants):
    con_prefix = r"""\textbf{"""
    con_suffix = r"""}"""

    con_prefix = ""
    con_suffix = ""

    string = ""
    for con in contestants[:-1]:
        string = string + con + ", "
    string += contestants[-1]

    return con_prefix + string + con_suffix

def betweenParanthesis(string):
    return string[string.find("(")+1:string.find(")")]

def extract_to_csv():
    try:
        remove(FILENAME)
    except OSError:
        pass

    MYSQL_CON = mdb.connect('localhost', 'andesil', 'password', 'gentleidi')
    with MYSQL_CON: 
        cur = MYSQL_CON.cursor()
        
        cur.execute(SQL_FETCH_USERNAME_TEAM)
        rows = cur.fetchall()
        fp = open(FILENAME, 'w')
        file = csv.writer(fp)
        file.writerows(rows)
        fp.close()

        #MYSQL_CON.commit()
        cur.close()
        #MYSQL_CON.close()

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
