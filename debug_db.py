#!/usr/bin/env python
import os
import sys

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jamaliweb_project.settings')

import django
django.setup()

from django.conf import settings
from django.db import connection
from django.core.management import execute_from_command_line

def debug_database():
    print("=== Database Debug Information ===")
    
    # Environment variables
    print(f"ENVIRONMENT: {os.environ.get('ENVIRONMENT', 'Not set')}")
    print(f"DATABASE_URL: {'Set' if os.environ.get('DATABASE_URL') else 'Not set'}")
    if os.environ.get('DATABASE_URL'):
        # Show first 50 chars of DATABASE_URL for debugging (hide sensitive info)
        db_url = os.environ.get('DATABASE_URL')
        print(f"DATABASE_URL preview: {db_url[:50]}...")
    print(f"DEBUG: {settings.DEBUG}")
    
    # Database configuration
    db_config = settings.DATABASES['default']
    print(f"\nDatabase Configuration:")
    print(f"  Engine: {db_config['ENGINE']}")
    print(f"  Name: {db_config.get('NAME', 'N/A')}")
    print(f"  Host: {db_config.get('HOST', 'N/A')}")
    print(f"  Port: {db_config.get('PORT', 'N/A')}")
    print(f"  User: {db_config.get('USER', 'N/A')}")
    
    # Test connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print("\n✅ Database connection successful!")
            
            # Check if tables exist
            if 'postgresql' in db_config['ENGINE']:
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    ORDER BY table_name
                """)
            else:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
            
            tables = cursor.fetchall()
            print(f"📋 Found {len(tables)} tables")
            for table in tables:
                print(f"  - {table[0]}")
            
            # Check specifically for pages_project table
            table_names = [table[0] for table in tables]
            if 'pages_project' in table_names:
                print("\n✅ pages_project table exists!")
            else:
                print("\n❌ pages_project table NOT found!")
                
            # Check migration status
            print(f"\n=== Migration Status ===")
            try:
                cursor.execute("SELECT * FROM django_migrations WHERE app='pages' ORDER BY id")
                migrations = cursor.fetchall()
                print(f"Applied pages migrations: {len(migrations)}")
                for migration in migrations:
                    print(f"  - {migration[2]} ({migration[3]})")
            except Exception as e:
                print(f"Error checking migrations: {e}")
                
    except Exception as e:
        print(f"\n❌ Database connection failed: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    debug_database() 