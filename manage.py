#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    current_environment=os.environ.get('DJANGO_ENVIRONMENT')
    if not current_environment:
        current_environment = 'development'

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'btools.settings.{}'.format(current_environment))
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
