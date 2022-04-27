#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    
    if 'main' in os.getcwd():
        print(os.getcwd())
        print("In Production Environment")
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jumpnow.settings.production')
    elif 'qa' in os.getcwd():
        print(os.getcwd())
        print("In Stage Environment")
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jumpnow.settings.qa')
    else:
        print(os.getcwd())
        print("In Dev Environment")
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jumpnow.settings.dev')    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
