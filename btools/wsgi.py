"""
WSGI config for btools project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

current_environment=os.environ.get('DJANGO_ENVIRONMENT')
if not current_environment:
    current_environment = 'development'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'btools.settings.{}'.format(current_environment))

application = get_wsgi_application()
