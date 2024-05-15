#!/bin/bash

# Based on: https://gist.github.com/mjambon/79adfc5cf6b11252e78b75df50793f24

# Run postgres in the background
./run-postgres.sh

cd backend

# Run the development server
poetry run python manage.py migrate

pids=()

# If WORKER_MODE is "True", we sync with the manager.
if [ "$WORKER_MODE" = "True" ]; then
    until poetry run python manage.py sync --host "$MANAGER_HOST" --port 8001; do
        echo "Manager is unavailable - sleeping"
        sleep 1
    done
else
    # Create a superuser for the manager
    poetry run python manage.py createsuperuser \
        --noinput \
        --username admin \
        --email admin@example.com
fi

SYNC_EXPOSED="True" poetry run python manage.py runserver 0.0.0.0:8001 &
pids+=($!)

SYNC_EXPOSED="False" poetry run python manage.py runserver 0.0.0.0:8000 &
pids+=($!)

# 'set -e' tells the shell to exit if any of the foreground command fails,
# i.e. exits with a non-zero status.
set -eu

# Wait for each specific process to terminate.
# Instead of this loop, a single call to 'wait' would wait for all the jobs
# to terminate, but it would not give us their exit status.
#
for pid in "${pids[@]}"; do
  #
  # Waiting on a specific PID makes the wait command return with the exit
  # status of that process. Because of the 'set -e' setting, any exit status
  # other than zero causes the current shell to terminate with that exit
  # status as well.
  #
  wait "$pid"
done
