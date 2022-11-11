## makefile
The windows batch file calls ticket_gen.py, store_tickets.py and SQLScript.sql consecutively. Because ticket_gen.py requires 2 input arguments, the makefile also requires 2 arguments.
E.g 'makefile 50 activities.json' will generate 50 tickets and store them in activities.json

### ticket_gen
ticket_gen.py generates an input number of tickets and stores them in a json file. 
-o and -n arguments are required.
E.g 'python ticket_gen.py -n 100 -o activities.json' will generate 100 tickets and store them in activities.json

### store_tickets
store_tickets.py reads in the data from 'activities.json' and stores them in the SQLite database 'tickets.db'

### SQLScipt
SQLScript.sql writes an SQL script that is run on the database 'tickets.db', generating time metrics for each ticket