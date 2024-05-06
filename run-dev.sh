#!/bin/bash

# Run postgres in the background
./run-postgres.sh

# Run the development server
cd backend
poetry run python manage.py migrate

# If WORKER_MODE is "True", we sync with the manager.
if [ "$WORKER_MODE" = "True" ]; then
    until poetry run python manage.py sync --host "$MANAGER_HOST" --port 8001; do
        echo "Manager is unavailable - sleeping"
        sleep 1
    done
fi

(SYNC_EXPOSED="True" poetry run python manage.py runserver 0.0.0.0:8001; [ "$?" -lt 2 ] && kill "$$") &
(SYNC_EXPOSED="False" poetry run python manage.py runserver 0.0.0.0:8000; [ "$?" -lt 2 ] && kill "$$") &
wait