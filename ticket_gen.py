import json
import random
import time
import argparse
import datetime
from datetime import timedelta

status_options = ["Open", "Waiting for Customer", "Waiting for Third Party", "Pending", "Resolved","Closed"]
category_options = ["Phone", "Computer", "iPad"]
product_options = ["mobile", "computer", "laptop", "iPad"]
group_options = ["buy", "sell", "refund"]
time_format = '%Y-%m-%d %H:%M:%S'
date_format = '%d %b, %Y'
end_at = datetime.datetime.now().strftime(time_format)
date_now = datetime.datetime.now().strftime(date_format)
start_at = (datetime.datetime.now() - timedelta(days=1)).strftime(time_format)


def generate_random_time():
    global start_at
    global end_at
    stime = time.mktime(time.strptime(start_at, time_format))
    etime = time.mktime(time.strptime(end_at, time_format))

    random_time_float = stime + random.random() * (etime - stime)

    random_time = datetime.datetime.fromtimestamp(random_time_float, tz=datetime.timezone.utc)
    random_time_date_format = datetime.datetime.fromtimestamp(random_time_float, tz=datetime.timezone.utc)

    return random_time.strftime(time_format), random_time_date_format.strftime(date_format)

def generate_time_between_times(start, end):
    time_float = start + random.random() * (end - start)
    time_datetime = datetime.datetime.fromtimestamp(time_float, tz=datetime.timezone.utc)
    time_string = time_datetime.strftime(time_format)
    return time_float, time_string


def generate_times(start, end):
    global start_at
    global end_at
    stime = time.mktime(time.strptime(start_at, time_format))
    etime = time.mktime(time.strptime(end_at, time_format))

    open_time_float, open_time = generate_time_between_times(stime, etime)
    customer_time_float, customer_time = generate_time_between_times(open_time_float, etime)
    pending_time_float, pending_time = generate_time_between_times(customer_time_float, etime)
    resolved_time_float, resolved_time = generate_time_between_times(pending_time_float, etime)
    third_party_time_float, third_party_time = generate_time_between_times(resolved_time_float, etime)
    closed_time_float, closed_time = generate_time_between_times(third_party_time_float, etime)

    return [open_time, customer_time, pending_time, resolved_time, third_party_time, closed_time]



def generate_ticket(uniqueTicketNumber, ticket_array):
    ticket_times = generate_times(start_at, end_at)
    for activityIndex in range(len(status_options)):
        status = status_options[activityIndex]
        performed_at = ticket_times[activityIndex]
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
                "shipment_date": date_now,
                "category": random.choice(category_options),
                "contacted_customer": bool(random.getrandbits(1)),
                "issue_type": "Incident",
                "source": random.randint(1,10),
                "status": status,
                "priority": random.randint(1,10),
                "group": random.choice(group_options),
                "agent_id": random.randint(1,1000000),
                "requester": random.randint(1,10000000),
                "product": random.choice(product_options),
            }
        }
        ticket_array.append(ticket_object)
    return

def create_all_tickets(ticket_numbers):
    uniqueTicketIDs = random.sample(range(1,10000),ticket_numbers)
    ticket_array = []
    for ticketIndex in range(ticket_numbers):
        
        uniqueTicketNumber = uniqueTicketIDs[ticketIndex]
        generate_ticket(uniqueTicketNumber, ticket_array)

    all_tickets = {
        "metadata": {
            "start_at": start_at,
            "end_at": end_at,
            "activities_count": ticket_numbers*len(status_options)
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
    try:
        output_file = arguments.out
        all_tickets = create_all_tickets(ticket_numbers)
        write_to_json(output_file, all_tickets)
    except Exception as e:
        print("Exception when writing to JSON file: {}".format(e))