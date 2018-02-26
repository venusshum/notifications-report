export FLASK_APP=application.py
export SQLALCHEMY_DATABASE_URI='postgresql://localhost/notify_reports'
export FLASK_DEBUG=1
export WERKZEUG_DEBUG_PIN=off
export NOTIFY_ENVIRONMENT='tests'
export STATSD_PREFIX='stats-prefix'
export NOTIFICATION_QUEUE_PREFIX='testing'
