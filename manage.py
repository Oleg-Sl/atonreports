#!/usr/bin/env python
"""Django's command-line utility for administrative save_data_from_bx24."""
import os
import sys


def main():
    """Run administrative save_data_from_bx24."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'atonreports.settings')
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
