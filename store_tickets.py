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
    def __init__(self, performed_at, ticket_id, performer_type, performer_id, activity):
        self.performed_at = performed_at
        self.ticket_id = ticket_id
        self.performer_type = performer_type
        self.performer_id = performer_id
        self.activity = Activity(**activity)
    
    def __repr__(self):
        return "ticket('{}', '{}', '{}', '{}', '{}')".format(self.performed_at, self.ticket_id, self.performer_type, self.performer_id, self.activity)

class Activity:
    def __init__(self, note, shipping_address, shipment_date, category, contacted_customer, issue_type, source, status, priority, group, agent_id, requester, product):
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
        return "activity('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(self.note, self.shipping_address, self.shipment_date, 
        self.category, self.contacted_customer,self.issue_type, self.source, self.status, self.priority, self.group, self.agent_id, self.requester, self.product)

class Note:
    def __init__(self, id, type):
        self.id = id
        self.type = type
    
    def __repr__(self):
        return "note('{}', '{}')".format(self.id, self.type)

def create_tables(conn, c):
    with conn:

        c.execute("""CREATE TABLE metadata (
                start_at text,
                end_at integer,
                activities_count integer
                ) """)

        c.execute("""CREATE TABLE tickets (
                performed_at text,
                ticket_id integer,
                performer_type text,
                performer_id integer,
                PRIMARY KEY (ticket_id)
                ) """)
        
        c.execute("""CREATE TABLE activities (
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
            PRIMARY KEY (ticket_id),
            FOREIGN KEY (ticket_id)
                REFERENCES tickets (ticket_id)
            ) """)

        c.execute("""CREATE TABLE notes (
            id integer,
            ticket_id integer,
            type integer,
            PRIMARY KEY (id),
            FOREIGN KEY (ticket_id)
                REFERENCES activities (ticket_id)
            ) """)


def insert_metadata(conn, c, metadata):
    with conn:
        c.execute("INSERT INTO metadata VALUES (:start_at, :end_at, :activities_count)", {'start_at': metadata.start_at, 
        'end_at': metadata.end_at, 'activities_count': metadata.activities_count})

def insert_ticket(conn, c, ticket):
    with conn:
        c.execute("INSERT INTO tickets VALUES (:performed_at, :ticket_id, :performer_type, :performer_id)", {'performed_at': ticket.performed_at, 
        'ticket_id': ticket.ticket_id, 'performer_type': ticket.performer_type, 'performer_id': ticket.performer_id})

        c.execute("INSERT INTO activities VALUES (:ticket_id, :shipping_address, :shipment_date, :category, :contacted_customer, :issue_type, \
        :source, :status, :priority, :group_option, :agent_id, :requester, :product)", {'ticket_id': ticket.ticket_id,
        'shipping_address': ticket.activity.shipping_address, 'shipment_date': ticket.activity.shipment_date, 'category': ticket.activity.category, 
        'contacted_customer': ticket.activity.contacted_customer, 'issue_type': ticket.activity.issue_type, 'source': ticket.activity.source, 
        'status': ticket.activity.status, 'priority': ticket.activity.priority, 'group_option': ticket.activity.group, 'agent_id': ticket.activity.agent_id,
        'requester': ticket.activity.requester, 'product': ticket.activity.product})

        c.execute("INSERT INTO notes VALUES (:id, :ticket_id, :type)", {'id': ticket.activity.note.id, 'ticket_id': ticket.ticket_id, 
        'type': ticket.activity.note.type})
        


if __name__ == '__main__':
    
    f = open('activities.json', 'r')
    jsonData = json.load(f)
    conn = sqlite3.connect('tickets.db')
    c = conn.cursor()

    create_tables(conn, c)

    metadata = jsonData['metadata']
    metadataObject = Metadata(**metadata)
    insert_metadata(conn, c, metadataObject)

    for ticket in jsonData['activities_data']:
        ticketObject = Ticket(**ticket)
        insert_ticket(conn, c, ticketObject)

    conn.close()
    f.close()