#!/bin/bash

# Run postgres in the background
./run-postgres.sh

# Run the development server
cd backend
poetry run python manage.py migrate

(SYNC_EXPOSED="True" poetry run python manage.py runserver 0.0.0.0:8001; [ "$?" -lt 2 ] && kill "$$") &
(SYNC_EXPOSED="False" poetry run python manage.py runserver 0.0.0.0:8000; [ "$?" -lt 2 ] && kill "$$") &
wait