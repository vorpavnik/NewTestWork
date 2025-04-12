import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewTestWork.settings')

app = Celery('NewTestWork')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

from .celery_schedule import CELERYBEAT_SCHEDULE  # Импортируйте расписание
app.conf.beat_schedule = CELERYBEAT_SCHEDULE  # Установите расписание