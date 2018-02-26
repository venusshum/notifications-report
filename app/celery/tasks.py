from app import notify_celery
from app.db_update.update_service import upsert_service
from app.db_update.update_template import upsert_template
from app.db_update.update_notification import upsert_notification

@notify_celery.task(name="update-reports-service-db")
def upsert_reports_service_db(report_data):
    print(report_data)
    upsert_service(report_data)


@notify_celery.task(name="update-reports-template-db")
def upsert_reports_template_db(report_data):
    print(report_data)
    upsert_template(report_data)


@notify_celery.task(name="update-reports-notification-db")
def upsert_reports_notification_db(report_data):
    print(report_data)
    upsert_notification(report_data)
