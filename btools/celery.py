import os
from celery import Celery

current_environment=os.environ.get('DJANGO_ENVIRONMENT')
if not current_environment:
    current_environment = 'development'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'btools.settings.{}'.format(current_environment))

app = Celery('btools')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))