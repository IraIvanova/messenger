import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery(
    'project',
    broker='redis://redis:6379/0'
)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
