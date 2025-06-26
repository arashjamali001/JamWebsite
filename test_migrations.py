#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jamaliweb_project.settings')
django.setup()

from django.core.management import execute_from_command_line

def test_migrations():
    print("=== Testing Migrations ===")
    
    # Check migration status
    print("1. Checking migration status...")
    try:
        execute_from_command_line(['manage.py', 'showmigrations'])
        print("✅ Migration status check successful")
    except Exception as e:
        print(f"❌ Migration status check failed: {e}")
        return
    
    # Try to run migrations
    print("\n2. Running migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate', '--noinput'])
        print("✅ Migrations completed successfully")
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    test_migrations() 