from celery import Celery
from celery.schedules import crontab
from django.core.management import call_command

app = Celery('yourapp')

@app.task
def save_daily_revenue():
    call_command('save_daily_revenue')

app.conf.beat_schedule = {
    'save_daily_revenue': {
        'task': 'yourapp.tasks.save_daily_revenue',
        'schedule': crontab(hour=0, minute=0),  # Run every day at midnight
    },
}
