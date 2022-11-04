## makefile
The windows batch file calls both ticket_gen.py and store_tickets.py consecutively. Because ticket_gen.py requires 2 input arguments, the makefile also requires 2 arguments.
E.g 'makefile 50 activities.json' will generate 50 tickets and store them in activities.json

### ticket_gen
ticket_gen.py generates an input number of tickets and stores them in a json file. 
-o and -n arguments are required.
E.g 'python ticket_gen.py -n 100 -o activities.json' will generate 100 tickets and store them in activities.json

### store_tickets
store_tickets.py reads in the data from 'activities.json' and stores them in the SQLite database 'tickets.db'
