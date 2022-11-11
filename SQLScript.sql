Create view if not exists entire_ticket as
select tickets_table.ticket_id, tickets_table.performed_at, activities_table.status
from tickets tickets_table
join activities activities_table on activities_table.activity_id = tickets_table.activity_id;

.headers on
select t1.ticket_id,
(strftime('%s', t2.performed_at)) - (strftime('%s', t1.performed_at)) as time_spent_open,
(strftime('%s', t3.performed_at)) - (strftime('%s', t2.performed_at)) as time_spent_waiting_on_customer,
(strftime('%s', t4.performed_at)) - (strftime('%s', t3.performed_at)) as time_spent_waiting_for_response,
(strftime('%s', t5.performed_at)) - (strftime('%s', t4.performed_at)) as time_till_resolution,
(strftime('%s', t6.performed_at)) - (strftime('%s', t5.performed_at)) as time_to_first_response



from entire_ticket t1
join entire_ticket t2 on t2.ticket_id = t1.ticket_id
join entire_ticket t3 on t3.ticket_id = t1.ticket_id
join entire_ticket t4 on t4.ticket_id = t1.ticket_id
join entire_ticket t5 on t5.ticket_id = t1.ticket_id
join entire_ticket t6 on t6.ticket_id = t1.ticket_id

where t1.status = 'Open'
and t2.status = 'Waiting for Customer'
and t3.status = 'Waiting for Third Party'
and t4.status = 'Pending'
and t5.status = 'Resolved'
and t6.status = 'Closed'

group by t1.ticket_id