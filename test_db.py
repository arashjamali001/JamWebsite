#!/usr/bin/env python
import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jamaliweb_project.settings')
django.setup()

from django.db import connection
from django.core.management import execute_from_command_line

def test_database():
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("Database connection successful!")
        
        # Test if tables exist
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cursor.fetchall()
        print(f"Found {len(tables)} tables: {[table[0] for table in tables]}")
        
    except Exception as e:
        print(f"Database error: {e}")

if __name__ == "__main__":
    test_database() 