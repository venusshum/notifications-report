#!/bin/bash
#
# Data ETL from notify-db used by api to notify-reports used by reports.
#
# This scripts is run locally. It will create temporary sql files, which will be imported to destination db
# This is a one-off migration. API and report app should be responsible for synchronising the DB thereafter.

cf target -s staging

#echo '---migrating service'
#cf conduit performance-test-notify-db -- pg_dump -t services -f service.sql
#cf conduit notify-reports -- psql < service.sql
#rm service.sql
#
#echo '---migrating organisation'
#cf conduit performance-test-notify-db -- pg_dump -t organisation -f organisation.sql
#cf conduit notify-reports -- psql < organisation.sql
#rm organisation.sql
#
#echo '--migrating organisation_to_service'
#cf conduit performance-test-notify-db -- pg_dump -t organisation_to_service -f organisation_to_service.sql
#cf conduit notify-reports -- psql < organisation_to_service.sql
#rm organisation_to_service.sql
#
#cf conduit performance-test-notify-db -- pg_dump -t templates -f templates.sql
#cf conduit notify-reports -- psql < templates.sql
#rm templates.sql
##
#cf conduit performance-test-notify-db -- pg_dump -t rates -f rates.sql
#cf conduit notify-reports -- psql < rates.sql
#rm rates.sql
#
#cf conduit performance-test-notify-db -- pg_dump -t provider_rates -f provider_rates.sql
#cf conduit notify-reports -- psql < provider_rates.sql
#rm provider_rates.sql
#
#cf conduit performance-test-notify-db -- pg_dump -t provider_details -f provider_details.sql
#cf conduit notify-reports -- psql < provider_details.sql
#rm provider_details.sql
##
cf conduit performance-test-notify-db -- pg_dump -t notifications -f notifications.sql
cf conduit notify-reports -- psql < notifications.sql
rm notifications.sql









