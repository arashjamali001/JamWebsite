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
from django.contrib.staticfiles.finders import find
from django.contrib.staticfiles.storage import staticfiles_storage

def check_static_files():
    print("=== Static Files Check ===")
    
    # Check if staticfiles directory exists
    static_root = settings.STATIC_ROOT
    print(f"STATIC_ROOT: {static_root}")
    print(f"STATIC_ROOT exists: {os.path.exists(static_root)}")
    
    # Check if main.css exists in staticfiles
    main_css_path = os.path.join(static_root, 'css', 'main.css')
    print(f"main.css in staticfiles: {os.path.exists(main_css_path)}")
    
    # Check static file finders
    print(f"\nStatic file finders:")
    for finder in settings.STATICFILES_FINDERS:
        print(f"  - {finder}")
    
    # Check if main.css can be found
    main_css_found = find('css/main.css')
    print(f"\nmain.css found by finders: {main_css_found}")
    
    # Check if staticfiles storage can serve the file
    try:
        main_css_url = staticfiles_storage.url('css/main.css')
        print(f"main.css URL: {main_css_url}")
    except Exception as e:
        print(f"Error getting main.css URL: {e}")
    
    # List files in staticfiles directory
    if os.path.exists(static_root):
        print(f"\nFiles in {static_root}:")
        for root, dirs, files in os.walk(static_root):
            level = root.replace(static_root, '').count(os.sep)
            indent = ' ' * 2 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 2 * (level + 1)
            for file in files:
                print(f"{subindent}{file}")

if __name__ == "__main__":
    check_static_files() 