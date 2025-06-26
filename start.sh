#!/usr/bin/env bash

echo "Starting application..."

# Wait for database to be ready with retries
echo "Waiting for database connection..."
for i in {1..30}; do
    echo "Attempt $i/30: Testing database connection..."
    python -c "
import os
import sys
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jamaliweb_project.settings')
import django
django.setup()
from django.db import connection
try:
    with connection.cursor() as cursor:
        cursor.execute('SELECT 1')
    print('Database connection successful!')
    exit(0)
except Exception as e:
    print(f'Database connection failed: {e}')
    exit(1)
" && break || sleep 2
done

# Run migrations with better error handling
echo "Running migrations..."
python manage.py migrate --noinput --verbosity=2
if [ $? -ne 0 ]; then
    echo "Migration failed, trying again..."
    sleep 5
    python manage.py migrate --noinput --verbosity=2
fi
echo "Migrations completed."

# Test migrations specifically
echo "Testing migrations..."
python test_migrations.py

# Manual table creation as fallback
echo "Checking for missing tables..."
python create_tables.py

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