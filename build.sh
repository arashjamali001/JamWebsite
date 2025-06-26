#!/usr/bin/env bash
# exit on error
set -o errexit

# Set environment variables for build
export ENVIRONMENT=production
export DEBUG=0
export SECRET_KEY=django-insecure-temp-key-for-build-only
export DATABASE_URL=sqlite:///temp.db

pip install pipenv
pipenv install --deploy --system

# Create staticfiles directory if it doesn't exist
mkdir -p staticfiles

python manage.py collectstatic --noinput

# Only run migrations if DATABASE_URL is set (not during build)
if [ -n "$DATABASE_URL" ] && [ "$DATABASE_URL" != "sqlite:///temp.db" ]; then
    python manage.py migrate
else
    echo "Skipping migrations during build phase"
fi 