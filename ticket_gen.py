import json
import random
import time
import argparse
import datetime

status_options = ["Open", "Closed", "Resolved", "Waiting for Customer", "Waiting for Third Party", "Pending"]
time_format = '%d-%m-%Y %H:%M:%S'
date_format = '%d %b, %Y'
start_at = "20-04-2017 10:00:00"
end_at = "21-04-2017 09:59:59"


def generate_random_time():
    global start_at
    global end_at
    stime = time.mktime(time.strptime(start_at, time_format))
    etime = time.mktime(time.strptime(end_at, time_format))

    random_time_float = stime + random.random() * (etime - stime)

    random_time = datetime.datetime.fromtimestamp(random_time_float, tz=datetime.timezone.utc)
    random_time_date_format = datetime.datetime.fromtimestamp(random_time_float, tz=datetime.timezone.utc)

    return random_time.strftime(time_format), random_time_date_format.strftime(date_format),

def generate_ticket(uniqueTicketNumber):
    performed_at, shipment_date = generate_random_time()
    ticket_object = {
    "performed_at": performed_at,
        "ticket_id": uniqueTicketNumber,
        "performer_type": "user",
        "performer_id": random.randint(1,1000000),
        "activity": {
            "note": {
                "id": random.randint(1,10000000),
                "type": random.randint(0,10)
            },
            "shipping_address": "N/A",
            "shipment_date": shipment_date,
            "category": "Phone",
            "contacted_customer": bool(random.getrandbits(1)),
            "issue_type": "Incident",
            "source": random.randint(1,10),
            "status": random.choice(status_options),
            "priority": random.randint(1,10),
            "group": "refund",
            "agent_id": random.randint(1,1000000),
            "requester": random.randint(1,10000000),
            "product": "mobile"
        }
    }
    return ticket_object

def create_all_tickets(ticket_numbers):
    uniqueTicketIDs = random.sample(range(1,10000),ticket_numbers)
    ticket_array = []
    for ticketIndex in range(ticket_numbers):
        
        uniqueTicketNumber = uniqueTicketIDs[ticketIndex]

        ticket = generate_ticket(uniqueTicketNumber)
        ticket_array.append(ticket)
    all_tickets = {
        "metadata": {
            "start_at": start_at,
            "end_at": end_at,
            "activities_count": ticket_numbers
        },
        "activities_data": ticket_array
    }
    return all_tickets

def write_to_json(output_file, all_tickets):
    with open(output_file, "w") as write_file:
        json.dump(all_tickets, write_file, indent=4,separators=(',',': '))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--num", help = "number of tickets to generate", required = True, default = 0)
    parser.add_argument("-o", "--out", help = "output json file", required = True, default = "")
    
    arguments = parser.parse_args()

    try: 
        ticket_numbers = int(arguments.num)
    except:
        print("Error: -Invalid argument(s)")
    output_file = arguments.out
    all_tickets = create_all_tickets(ticket_numbers)
    write_to_json(output_file, all_tickets)