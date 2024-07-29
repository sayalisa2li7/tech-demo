#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Wait for the database to be ready
until python manage.py migrate; do
  >&2 echo "Waiting for the database to be ready..."
  sleep 3
done

# Create migrations and apply them
echo "Creating database migrations..."
python manage.py makemigrations

echo "Applying database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn processes
echo "Starting Gunicorn..."
gunicorn tech_demo.wsgi:application --bind 0.0.0.0:8000 --workers 3 &

# Start Celery worker
echo "Starting Celery worker..."
celery -A tech_demo worker --loglevel=info &

# Start Celery beat
echo "Starting Celery beat..."
celery -A tech_demo beat --loglevel=info &

# echo "Starting Celery flower..."
# celery -A tech_demo flower --port=5555 &

# Keep the container running
tail -f /dev/null
