#!/usr/bin/env bash

echo "Starting application..."


python manage.py migrate 
echo "Migrations completed."


# Run debug script
echo "Running database debug script..."
python debug_db.py

# Test database connection
echo "Testing database connection..."
python test_db.py

echo "Starting Gunicorn..."
gunicorn jamaliweb_project.wsgi:application --bind 0.0.0.0:$PORT 