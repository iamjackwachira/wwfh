#!/bin/bash

set -e

echo "Starting Server"

echo $(date -u) "- Migrating"
python3 manage.py migrate

echo $(date -u) "- Collecting static"
python3 manage.py collectstatic --noinput

echo $(date -u) "- Running the server"
gunicorn config.wsgi --config config/gunicorn_conf.py --log-level debug
