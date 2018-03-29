
insert into notifications_temp (notification_id, dm_service_year, dm_template, dm_datetime, rate_multiplier, crown,
notification_type, provider, provider_rate, client_rate, international, billable_units, notifications_sent)
select
n.id,
n.service_id,
n.template_id,
da.bst_date,
coalesce(n.rate_multiplier,1),
s.crown,
n.notification_type,
n.sent_by,
coalesce((select rate_tb.rate from
(select * from provider_rates left join provider_details on provider_rates.provider_id = provider_details.id) as rate_tb
where lower(n.sent_by) = lower(rate_tb.identifier) and n.sent_at > rate_tb.valid_from order by rate_tb.valid_from desc limit 1), 0),
coalesce((select rates.rate from rates
where n.notification_type = rates.notification_type and n.sent_at > rates.valid_from order by rates.valid_from desc limit 1), 0),
coalesce(n.international, false),
n.billable_units,
1
from public.notification_history n
left join dm_template t on t.template_id = n.template_id
left join dm_datetime da on n.created_at > da.utc_daytime_start and n.created_at < da.utc_daytime_end
left join dm_service_year s on s.service_id = n.service_id and s.financial_year = da."financial_year";


-- ft_billing:  Aggregate into billing fact table

delete from ft_billing where 1=1;   -- Note: delete this if we are already using ft_billing

insert into ft_billing (dm_service_year, dm_template, dm_datetime, notification_type, crown, provider, rate_multiplier,
provider_rate, client_rate, international, notifications_sent, billable_units)
select billing.dm_service_year, template.template_id, date.bst_date, billing.notification_type, billing.crown, billing.provider,
avg(billing.rate_multiplier), avg(billing.provider_rate), avg(client_rate), international,
count(*) as notifications_sent,
sum(billing.billable_units) as billable_units
from notifications_temp as billing
left join dm_template template on billing.dm_template = template.template_id
left join dm_datetime date on billing.dm_datetime = date.bst_date
group by date.bst_date, template.template_id, billing.dm_service_year, billing.provider, billing.notification_type, billing.international, billing.crown
order by date.bst_date;

-- update ft_billing set billing_total=billable_units*rate_multiplier*client_rate where 1=1;

update ft_billing set provider='DVLA' where notification_type = 'letter';

update dm_service_year set organisation='Not set' where organisation = null;

update dm_service_year set organisation_type='Not set' where organisation_type = NULL;