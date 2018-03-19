-- create a temp table, an intermediate step to transform data from notifications table to the format in ft_billing
-- Note: to run this script successfully, all templates need to be set.

-- populate dm_service
delete from dm_service_year where 1=1;
insert into dm_service_year (id, service_id, service_name, financial_year, free_sms_fragment_limit, organisation, crown, research_mode, restricted, organisation_type, created_at, updated_at, active)
(
	select
	uuid_in(md5(random()::text)::cstring ) as id,
	s.id as service_id,
	s.name as service_name,
	b.financial_year_start,
	b.free_sms_fragment_limit,
	coalesce(o.name, 'not defined') as organisation,
	(select
	 case when s.crown=true then 'crown'
	      when s.crown=false then 'non-crown'
	 end) as crown,
	s.research_mode,
	s.restricted,
	s.organisation_type,
	s.created_at,
	s.updated_at,
	s.active
	from services s
	left join organisation_to_service os on s.id = os.service_id
	left join organisation o on os.organisation_id = o.id
	right join annual_billing b on b.service_id = s.id
);

delete from dm_template where 1=1;
insert into dm_template
(
	select
	templates.id as template_id,
	templates.name as template_name,
	templates.template_type,
	templates.service_id as service_id
	from templates
);

drop table if exists notifications_temp;

--create type notification_type as enum('email', 'sms', 'letter');

create table notifications_temp (
	notification_id uuid,
	dm_template uuid,
	dm_datetime date,
	dm_service_year uuid,
	notification_type notification_type,
	provider varchar,
	rate_multiplier numeric,
	crown varchar,
	provider_rate numeric,
	client_rate numeric,
	international bool,
	billable_units numeric,
	notifications_sent numeric
);


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