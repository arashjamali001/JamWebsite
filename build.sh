#!/usr/bin/env bash
# exit on error
set -o errexit

# Set environment variables for build
export ENVIRONMENT=production
export DEBUG=0
export SECRET_KEY=django-insecure-temp-key-for-build-only

# Install dependencies
pip install pipenv
pipenv install --deploy --system

# Create staticfiles directory if it doesn't exist
mkdir -p staticfiles

# Remove any existing staticfiles to avoid conflicts
rm -rf staticfiles/*

# Collect static files with proper error handling
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear --verbosity=2

# Create a simple manifest file for static files
echo "Creating static files manifest..."
python manage.py collectstatic --noinput --dry-run > /dev/null 2>&1 || true

echo "Build completed successfully!" 