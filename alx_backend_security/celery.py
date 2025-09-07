import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "alx_backend_security.settings")

app = Celery("alx_backend_security")

# Load task-related settings from Django settings.py
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks in all installed apps
app.autodiscover_tasks()

# Define periodic tasks (Celery Beat)
app.conf.beat_schedule = {
    "detect-suspicious-ips-every-hour": {
        "task": "ip_tracking.tasks.detect_suspicious_ips",
        "schedule": crontab(minute=0, hour="*"),
    },
}
