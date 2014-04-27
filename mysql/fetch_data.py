import MySQLdb as mdb
from collections import defaultdict
from subprocess import Popen
from shlex import split

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

MYSQL_CON = mdb.connect('localhost', 'root', '12345', 'gentleidi');

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

def process_team_contestants():
    for team_name, contestants in get_team_contestant_dict().iteritems():
        tex_dict = {
               betweenParanthesis(CONTESTANT_PARSELINE) : renderingStr(contestants),
               betweenParanthesis(TEAM_PARSELINE)       : team_name}

        with open('cover.tex','w') as f:
            f.write(LATEX_PARSE%tex_dict)

    proc=Popen(split('pdflatex cover.tex'))
    proc.communicate()

def extract_to_csv():
    #INTO OUTFILE '/tmp/out", DATE_FORMAT(now(),'%d-%h%s'), ".csv' 
    #
    SQL_TO_CSV = """
SELECT @sql_cmd := concat("
SELECT T.name, U.email 
    INTO OUTFILE '/tmp/FILE", DATE_FORMAT(now(),'%d-%h%s'), ".csv' 
    FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' 
FROM contest_team AS T , userregistration_customuser AS U, contest_team_members AS CTM 
WHERE CTM.team_id = T.id AND U.id = CTM.customuser_id AND T.onsite = 1 ;
");
PREPARE stmt FROM @sql_cmd;
EXECUTE stmt;
"""
    with MYSQL_CON: 
        cur = MYSQL_CON.cursor()
        
        #import ipdb; ipdb.set_trace()
        cur.execute(SQL_TO_CSV)
        cur.close()


    MYSQL_CON.commit()
    MYSQL_CON.close()

if __name__ == "__main__":
    #process_team_contestants()
    extract_to_csv()


# EOF
