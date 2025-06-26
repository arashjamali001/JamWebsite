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

python manage.py collectstatic --noinput
python manage.py migrate 