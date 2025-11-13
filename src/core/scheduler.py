from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from .jobs import export_data

scheduler = BackgroundScheduler(timezone=str(timezone.get_current_timezone()))

def start():
    global scheduler
    if not scheduler.running: 
        scheduler = BackgroundScheduler(timezone=str(timezone.get_current_timezone()))
        scheduler.add_job(
            export_data,
            'cron',
            hour=19,
            minute=0
        )
        scheduler.start()