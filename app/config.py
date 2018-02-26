import os
import json
from kombu import Exchange, Queue

def extract_cloudfoundry_config():
    vcap_services = json.loads(os.environ['VCAP_SERVICES'])
    set_config_env_vars(vcap_services)


def set_config_env_vars(vcap_services):
    # Postgres config
    os.environ['SQLALCHEMY_DATABASE_URI'] = vcap_services['postgres'][0]['credentials']['uri']
    vcap_application = json.loads(os.environ['VCAP_APPLICATION'])
    os.environ['NOTIFY_ENVIRONMENT'] = vcap_application['space_name']
    os.environ['NOTIFY_LOG_PATH'] = '/home/vcap/logs/app.log'



if os.environ.get('VCAP_SERVICES'):
    # on cloudfoundry, config is a json blob in VCAP_SERVICES - unpack it, and populate
    # standard environment variables from it
    extract_cloudfoundry_config()


class Config(object):
    NOTIFICATION_QUEUE_PREFIX = os.getenv('NOTIFICATION_QUEUE_PREFIX')

    # DB conection string
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
    AWS_REGION = os.getenv('AWS_REGION', 'eu-west-1')
    BROKER_URL = 'sqs://'
    BROKER_TRANSPORT_OPTIONS = {
        'region': AWS_REGION,
        'polling_interval': 1,
        'visibility_timeout': 310,
        'queue_name_prefix': NOTIFICATION_QUEUE_PREFIX
    }
    CELERY_ENABLE_UTC = True
    CELERY_TIMEZONE = 'Europe/London'
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_IMPORTS = ('app.celery.tasks',)
    # restart workers after each task is executed - this will help prevent any memory leaks (not that we should be
    # encouraging sloppy memory management). Since we only run a handful of tasks per day, and none are time sensitive,
    # the extra couple of seconds overhead isn't seen to be a huge issue.
    CELERYD_MAX_TASKS_PER_CHILD = 1
    CELERY_QUEUES = [
        Queue('reports-tasks', Exchange('default'), routing_key='reports-tasks')
    ]


class Development(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class Preview(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class Staging(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class Live(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class CloudFoundryConfig(Config):
    pass


class Sandbox(CloudFoundryConfig):
    SQLALCHEMY_TRACK_MODIFICATIONS = True


configs = {
    'development': Development,
    'sandbox': Sandbox,
    'preview': Preview,
    'staging': Staging,
    'production': Live

}
