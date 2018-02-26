#!/bin/bash

set -e

source environment_slicer.sh

# TODO: shouldn't need these but not sure why it won't work otherwise
# export FLASK_APP=application.py
# export SQLALCHEMY_DATABASE_URI='postgresql://localhost/notify_reports'

flask run -p 6019

