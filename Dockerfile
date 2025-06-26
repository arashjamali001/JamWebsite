# Pull base image
From python:3.11-slim

# Install system dependencies required for Pillow and other common packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    python3-dev \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    libfreetype6-dev \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /code

# Install pipenv
RUN pip install pipenv

# Copy Pipenv files first for better caching
COPY Pipfile .
COPY Pipfile.lock .

# Install dependencies using pipenv
RUN pipenv install --deploy --system

# Copy the rest of your project
COPY . .

# Expose port
EXPOSE 8000

# Default command for Render
CMD gunicorn jamaliweb_project.wsgi:application --bind 0.0.0.0:$PORT
