#!/bin/bash
#
# Data ETL from notify-db used by api to notify-reports used by reports.
#
# This scripts is run locally. It will create temporary sql files, which will be imported to destination db
# This is a one-off migration. API and report app should be responsible for synchronising the DB thereafter.

#pg_dump -t services notification_api -f services.sql
#psql notify_reports -f services.sql
#rm services.sql
#
#pg_dump -t organisation notification_api -f organisation.sql
#psql notify_reports -f organisation.sql
#rm organisation.sql
#
#pg_dump -t organisation_to_service notification_api -f org_to_service.sql
#psql notify_reports -f org_to_service.sql
#rm org_to_service.sql
##
#pg_dump -t templates notification_api -f templates.sql
#psql notify_reports -f templates.sql
#rm templates.sql
#
#pg_dump -t rates notification_api -f rates.sql
#psql notify_reports -f rates.sql
#rm rates.sql
#
#pg_dump -t annual_billing notification_api -f annual_billing.sql
#psql notify_reports -f annual_billing.sql
#rm annual_billing.sql
#
#pg_dump -t provider_rates notification_api -f provider_rates.sql
#psql notify_reports -f provider_rates.sql
#rm provider_rates.sql

##
#pg_dump -t provider_details notification_api -f provider_details.sql
#psql notify_reports -f provider_details.sql
#rm provider_details.sql
#
#pg_dump -t notifications notification_api -f notifications.sql
#psql notify_reports -f notifications.sql
#rm notifications.sql

pg_dump -t notification_history notification_api -f notification_history.sql
psql notify_reports -f notification_history.sql
rm notification_history.sql










