#!/usr/bin/env bash

echo "Starting application..."

# Check if DATABASE_URL is set
if [ -n "$DATABASE_URL" ]; then
    echo "DATABASE_URL is set, running migrations..."
    python manage.py migrate
else
    echo "WARNING: DATABASE_URL is not set!"
fi

# Test database connection
echo "Testing database connection..."
python test_db.py

echo "Starting Gunicorn..."
gunicorn jamaliweb_project.wsgi:application --bind 0.0.0.0:$PORT 