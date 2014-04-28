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


from openshift.helpFunctions.views import get_most_plausible_contest 
from openshift.contest.models import Team, Contest

# local import
from latex_file import CONTESTANT_PARSELINE, TEAM_PARSELINE, LATEX_PARSE

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
MYSQL_CON = mdb.connect('localhost', 'tino', 'password', 'gentleidi')




def process_team_contestants(request):
    team_contestant_dict = get_team_contestant_dict()
    # yesno = raw_input("This will make latex for each %s teams - are you sure?"
    #                  % (len(team_contestant_dict)) +  "(Y/N)\n" )
    # if yesno is not 'Y':
    #     return

    dir_dest = "/tmp/teams/"
    if not path.exists(dir_dest):
        makedirs(dir_dest)

    pattern = re.compile('[\W_]+')

    i = 0
    for team_name, contestants in team_contestant_dict.iteritems():
        tex_dict = {
               betweenParanthesis(CONTESTANT_PARSELINE) : renderingStr(contestants),
               betweenParanthesis(TEAM_PARSELINE)       : team_name}

        file_name = dir_dest + pattern.sub('', team_name) +  str(i) + '.tex'
    
        i += 1

        with open(file_name,'w') as f:
            f.write(LATEX_PARSE%tex_dict)

        proc=Popen(split('pdflatex -output-directory %s ' % (dir_dest) + file_name))
        proc.communicate()

    s = StringIO()
    #ZIP_FILE = "/tmp/teams.zip"
    zf = ZipFile(s, mode='w')

    pdf_files = [file for file in listdir(dir_dest) if file.endswith(".pdf")]
    for pdf in pdf_files:
        zf.write(path.join(dir_dest, pdf))
    zf.close()

    # Grab ZIP file from in-memory, make response with correct MIME-type
    response = HttpResponse(s.getvalue(), mimetype = "application/x-zip-compressed")
    # ..and correct content-disposition
    response['Content-Disposition'] = 'attachment; filename=%s' % zf.filename

    return response

def get_team_contestant_dict():
    team_members_dict = defaultdict( list )
    with MYSQL_CON: 
        cur = MYSQL_CON.cursor()
        cur.execute(SQL_FETCH_USERNAME_TEAM)

        rows = cur.fetchall()
        for row in rows:
            team, user = row[0], row[1]
            team_members_dict[team].append(user)
    return team_members_dict

def renderingStr(contestants):
    con_prefix = r"""\textbf{"""
    con_suffix = r"""}"""
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

    with MYSQL_CON: 
        cur = MYSQL_CON.cursor()
        
        #import ipdb; ipdb.set_trace()
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
