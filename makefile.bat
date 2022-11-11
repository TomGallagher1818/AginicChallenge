@ECHO OFF
IF %1.==. GOTO InvalidArg
IF %2.==. GOTO InvalidArg

python ticket_gen.py -n %1 -o %2
python store_tickets.py
sqlite3 tickets.db ".read SQLScript.sql"

GOTO End1
:InvalidArg
  ECHO Invalid Arguments. Number of tickets and output file are required. 
  ECHO E.g 'makefile.bat 100 activities.json'
GOTO End1

:End1