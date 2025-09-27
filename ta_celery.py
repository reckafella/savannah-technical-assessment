from os import environ
from celery import Celery


environ.setdefault('DJANGO_SETTINGS_MODULE', 'savannah_project.settings')

app = Celery('savannah_project')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()