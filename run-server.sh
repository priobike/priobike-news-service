#!/bin/bash

# Run postgres in the background
./run-postgres.sh

# Run gunicorn
cd backend

(SYNC_EXPOSED="True" poetry run gunicorn backend.wsgi:application --workers 4 --bind 0.0.0.0:8001; [ "$?" -lt 2 ] && kill "$$") &
(SYNC_EXPOSED="False" poetry run gunicorn backend.wsgi:application --workers 4 --bind 0.0.0.0:8000; [ "$?" -lt 2 ] && kill "$$") &
wait