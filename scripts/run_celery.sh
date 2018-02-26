#!/bin/bash

set -e

source environment.sh
celery -A run_celery.notify_celery worker --pidfile="/tmp/celery-reports.pid" --loglevel=INFO --concurrency=1
