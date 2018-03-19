-- Migration records

cf marketplace -s postgres

cf create-service postgres Free notify-reports

cf push notify-reports-api -f manifest-reports-staging.yml

cf push notify-reports-db-migration -f manifest-reports-staging.yml

cf run-task notify-reports-db-migration "flask db upgrade" --name notify-reports_db_migration

./scripts/data_migration.sh
-- may want to migrate notifications in a seperate run

cf conduit notify-reports -- psql -f ./scripts/etl.sql

--Found out that primary constraint is stopping the etl. Perform
--alter table ft_billing drop constraint ft_billing_pkey;

cf push notify-reports-slicer -f manifest-reports-slicer-staging.yml
curl -u name:pass "https://notify-reports-slicer-staging.cloudapps.digital/cube/ft_billing/aggregate?drilldown=dm_datetime:year,service"