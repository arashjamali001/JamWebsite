#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jamaliweb_project.settings')
django.setup()

from django.db import connection
from django.core.management import execute_from_command_line

def create_tables():
    print("=== Manual Table Creation ===")
    
    try:
        # Check if pages_project table exists
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'pages_project'
                );
            """)
            exists = cursor.fetchone()[0]
            
            if exists:
                print("✅ pages_project table already exists")
                return
            
            print("❌ pages_project table does not exist")
            print("Attempting to create tables manually...")
            
            # Try to run migrations again
            execute_from_command_line(['manage.py', 'migrate', 'pages', '--noinput'])
            
            # Check again
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'pages_project'
                );
            """)
            exists = cursor.fetchone()[0]
            
            if exists:
                print("✅ pages_project table created successfully")
            else:
                print("❌ Failed to create pages_project table")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    create_tables() 