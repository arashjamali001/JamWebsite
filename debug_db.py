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

def debug_database():
    print("=== Database Debug Information ===")
    
    # Environment variables
    print(f"ENVIRONMENT: {os.environ.get('ENVIRONMENT', 'Not set')}")
    print(f"DATABASE_URL: {'Set' if os.environ.get('DATABASE_URL') else 'Not set'}")
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
                """)
            else:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            
            tables = cursor.fetchall()
            print(f"📋 Found {len(tables)} tables")
            for table in tables:
                print(f"  - {table[0]}")
                
    except Exception as e:
        print(f"\n❌ Database connection failed: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    debug_database() 