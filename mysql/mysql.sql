SET @sql_cmd := concat("
SELECT T.name, U.email 
    INTO OUTFILE '/tmp/out", DATE_FORMAT(now(),'%d-%h%s'), ".csv' 
    FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' 
FROM contest_team AS T , userregistration_customuser AS U, contest_team_members AS CTM 
WHERE CTM.team_id = T.id AND U.id = CTM.customuser_id AND T.onsite = 1 ;
");

PREPARE stmt FROM @sql_cmd;
EXECUTE stmt;
