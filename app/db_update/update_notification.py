import sqlalchemy
from flask import current_app
from datetime import datetime

fields_map = {
            'id':'notification_id',
            'dm_template':'template',
            'dm_service': 'service',
            'type': 'type',
            'provider': 'provider',
            'rate_multiplier': 'rate_multiplier',
            'created_at': 'created_at',
            'updated_at': 'updated_at'}


def transform_data(report_data):
    report_data['dm_datetime'] = report_data['create_at'].date()

    return report_data


def upsert_notification(report_data):
    connection_string = current_app.config.get('SQLALCHEMY_DATABASE_URI')
    db = sqlalchemy.create_engine(connection_string)
    engine = db.connect()
    meta = sqlalchemy.MetaData(engine)

    sql_statement = "select * from notifications_for_today where notification_id = '{}'".format(report_data['id'])
    result = engine.execute(sql_statement)
    report_data = transform_data(report_data)

    if result.rowcount == 0:
        sql_statement = "insert into notifications_for_today (notification_id) values ('{}')".format(report_data['id'])
        result = engine.execute(sql_statement)
        print(result)

    for field in fields_map:
        if field in report_data and report_data[field] is not None:
            sql_statement = "update notifications_for_today set {} = '{}' where notification_id = '{}'".format(fields_map[field], report_data[field], report_data['id'])
            result = engine.execute(sql_statement)

    engine.close()

# from app.db_update.update_template import upsert_template
# sql = {'created_by': 'venus.bailey@digital.cabinet-office.gov.uk', 'created_at': '2017-12-14T13:25:36.938471Z', 'version': 6, 'personalisation': {}, 'body': 'No content', 'name': 'Test1.6', 'updated_at': '2018-02-19T16:51:43.433569Z', 'subject': 'No subject', 'id': '2911d7dc-098c-4a56-9a7d-20bcb336dbfd', 'type': 'email'}
# upsert_template(sql)
