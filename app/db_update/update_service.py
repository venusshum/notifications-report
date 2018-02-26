import sqlalchemy
from flask import current_app
from datetime import datetime

service_fields_map = {
            'name':'service_name',
            'created_by': 'created_by_id',
            'crown': 'crown',
            'restricted':'restricted',
            'active': 'active',
            'email_from': ' email_from',
            'created_at': 'created_at',
            'updated_at': 'updated_at',
            'organisation': 'organisation',
            'organisation_type': 'organisation_type',
            'research_mode': 'research_mode'}


def transform_data(report_data):
    if 'crown' in report_data:
        report_data['crown'] = 'crown' if True else 'non-crown'
    if 'restricted' in report_data:
        report_data['restricted'] = 'trial' if True else 'live'
    if 'active' in report_data:
        report_data['active'] = 'active' if True else 'non-active'

    # Timestamp data
    if 'updated_at' not in report_data:
        report_data['updated_at'] = datetime.now()
    return report_data


def upsert_service(report_data):
    connection_string = current_app.config.get('SQLALCHEMY_DATABASE_URI')
    db = sqlalchemy.create_engine(connection_string)
    engine = db.connect()
    meta = sqlalchemy.MetaData(engine)
    sql_statement = "select * from dm_service where service_id = '{}'".format(report_data['id'])
    result = engine.execute(sql_statement)
    report_data = transform_data(report_data)

    if result.rowcount == 0:
        sql_statement = "insert into dm_service (service_id) values ('{}')".format(report_data['id'])
        result = engine.execute(sql_statement)


    for field in service_fields_map:
        if field in report_data:
            sql_statement = "update dm_service set {} = '{}' where service_id = '{}'".format(service_fields_map[field], report_data[field], report_data['id'])
            result = engine.execute(sql_statement)

    engine.close()
