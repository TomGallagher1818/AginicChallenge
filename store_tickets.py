import json
import sqlite3

class Metadata:
    def __init__(self, start_at, end_at, activities_count):
        self.start_at = start_at
        self.end_at = end_at
        self.activities_count = activities_count

    def __repr__(self):
        return "metadata('{}', '{}', '{}', '{}', '{}')".format(self.start_at, self.end_at, self.activities_count)


class Ticket:
    def __init__(self, id, performed_at, ticket_id, performer_type, performer_id, activity):
        self.id = id
        self.performed_at = performed_at
        self.ticket_id = ticket_id
        self.performer_type = performer_type
        self.performer_id = performer_id
        self.activity = Activity(id, **activity)
    
    def __repr__(self):
        return "ticket('{}', '{}', '{}', '{}', '{}', '{}')".format(self.id, self.performed_at, self.ticket_id, self.performer_type, self.performer_id, self.activity)

class Activity:
    def __init__(self, id, note, shipping_address, shipment_date, category, contacted_customer, issue_type, source, status, priority, group, agent_id, requester, product):
        self.id = id
        self.note = Note(**note)
        self.shipping_address = shipping_address
        self.shipment_date = shipment_date
        self.category = category
        self.contacted_customer = contacted_customer
        self.issue_type = issue_type
        self.source = source
        self.status = status
        self.priority = priority
        self.group = group
        self.agent_id = agent_id
        self.requester = requester
        self.product = product
    
    def __repr__(self):
        return "activity('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(self.note, self.id, self.shipping_address, self.shipment_date, 
        self.category, self.contacted_customer,self.issue_type, self.source, self.status, self.priority, self.group, self.agent_id, self.requester, self.product)

class Note:
    def __init__(self, id, type):
        self.id = id
        self.type = type
    
    def __repr__(self):
        return "note('{}', '{}')".format(self.id, self.type)

def create_tables(conn, c):
    with conn:

        c.execute("""CREATE TABLE IF NOT EXISTS metadata (
                start_at timestamp,
                end_at timestamp,
                activities_count integer
                ) """)

        c.execute("""CREATE TABLE IF NOT EXISTS tickets (
                id integer,
                ticket_id integer,
                performed_at timestamp,
                performer_type text,
                performer_id integer,
                activity_id integer,
                PRIMARY KEY (id),
                FOREIGN KEY (activity_id)
                    REFERENCES activities (activity_id)
                ) """)
        
        c.execute("""CREATE TABLE IF NOT EXISTS activities (
            activity_id integer,
            ticket_id integer,
            shipping_address text,
            shipment_date text,
            category text,
            contacted_customer BOOLEAN,
            issue_type text,
            source integer,
            status text,
            priority integer,
            group_option text,
            agent_id integer,
            requester integer,
            product text,
            PRIMARY KEY (activity_id),
            FOREIGN KEY (ticket_id)
                REFERENCES tickets (ticket_id)
            ) """)

        c.execute("""CREATE TABLE IF NOT EXISTS notes (
            id integer,
            ticket_id integer,
            type integer,
            PRIMARY KEY (id),
            FOREIGN KEY (ticket_id)
                REFERENCES activities (ticket_id)
            ) """)


def insert_metadata(conn, c, metadata):
    with conn:
        c.execute("INSERT OR IGNORE INTO metadata VALUES('{}', '{}', '{}')".format(metadata.start_at, metadata.end_at, metadata.activities_count))

def insert_ticket(conn, c, ticket):
    with conn:
        c.execute("INSERT OR IGNORE INTO tickets VALUES('{}', '{}', '{}', '{}', '{}', '{}')".format(ticket.id, ticket.ticket_id, ticket.performed_at, 
        ticket.performer_type, ticket.performer_id, ticket.activity.id))
    
        c.execute("INSERT OR IGNORE INTO activities VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
            ticket.activity.id, ticket.id, ticket.activity.shipping_address, ticket.activity.shipment_date,ticket.activity.category, ticket.activity.contacted_customer,
            ticket.activity.issue_type, ticket.activity.source, ticket.activity.status, ticket.activity.priority, ticket.activity.group, ticket.activity.agent_id,
            ticket.activity.requester,ticket.activity.product))
        
        c.execute("INSERT OR IGNORE INTO notes VALUES('{}', '{}', '{}')".format(ticket.activity.note.id, ticket.ticket_id, ticket.activity.note.type))
        


if __name__ == '__main__':
    
    f = open('activities.json', 'r')
    jsonData = json.load(f)
    conn = sqlite3.connect('tickets.db')
    c = conn.cursor()

    create_tables(conn, c)

    metadata = jsonData['metadata']
    metadataObject = Metadata(**metadata)
    insert_metadata(conn, c, metadataObject)
    id = 1
    for ticket in jsonData['activities_data']:
        ticketObject = Ticket(id, **ticket)
        
        insert_ticket(conn, c, ticketObject)
        id += 1
    
    conn.close()
    f.close()