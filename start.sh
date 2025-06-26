#!/usr/bin/env bash

echo "Starting application..."

# Wait a moment for database to be ready
sleep 2

# Run migrations first
echo "Running migrations..."
python manage.py migrate --noinput
echo "Migrations completed."

# Test migrations specifically
echo "Testing migrations..."
python test_migrations.py

# Collect static files if needed
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Check static files
echo "Checking static files..."
python check_static.py

# Run debug script
echo "Running database debug script..."
python debug_db.py

# Test database connection
echo "Testing database connection..."
python test_db.py

echo "Starting Gunicorn..."
gunicorn jamaliweb_project.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120 