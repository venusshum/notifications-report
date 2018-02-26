#!/bin/bash

set -e -o pipefail

TERMINATE_TIMEOUT=30

function check_params {
  if [ -z "${NOTIFY_APP_NAME}" ]; then
    echo "You must set NOTIFY_APP_NAME"
    exit 1
  fi

  if [ -z "${CW_APP_NAME}" ]; then
    CW_APP_NAME=${NOTIFY_APP_NAME}
  fi
}


function on_exit {
  echo "Terminating application process with pid ${APP_PID}"
  kill ${APP_PID} || true
  n=0
  while (kill -0 ${APP_PID} 2&>/dev/null); do
    echo "Application is still running.."
    sleep 1
    let n=n+1
    if [ "$n" -ge "$TERMINATE_TIMEOUT" ]; then
      echo "Timeout reached, killing process with pid ${APP_PID}"
      kill -9 ${APP_PID} || true
      break
    fi
  done
  echo "Terminating remaining subprocesses.."
  kill 0
}

function start_application {
  exec "$@" &
  APP_PID=`jobs -p`
  echo "Application process pid: ${APP_PID}"
}


function run {
  while true; do
    kill -0 ${APP_PID} 2&>/dev/null || break
    sleep 1
  done
}

echo "Run script pid: $$"

check_params

trap "on_exit" EXIT


# The application has to start first!
start_application "$@"

run
