import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfolio_website.settings")

app = Celery("portfolio_website")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
    
app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'