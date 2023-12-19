import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


def get_celery_worker_status():
    i = app.control.inspect()
    availability = i.ping()
    # stats = i.stats()
    # registered_tasks = i.registered()
    # active_tasks = i.active()
    # scheduled_tasks = i.scheduled()
    result = {
        'availability': availability,
        # 'stats': stats,
        # 'registered_tasks': registered_tasks,
        # 'active_tasks': active_tasks,
        # 'scheduled_tasks': scheduled_tasks
    }
    return result