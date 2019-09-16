""" Export Celery Task Queue """

from .celery import app as celery_app

__all__ = ('celery_app',)
