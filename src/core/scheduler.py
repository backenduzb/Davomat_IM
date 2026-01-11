from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from .jobs import export_data

scheduler = BackgroundScheduler(timezone=str(timezone.get_current_timezone()))

def start():
    global scheduler

    if not scheduler.running:
        scheduler.start()

    if not scheduler.get_job("export_job"):
        scheduler.add_job(
            export_data,
            'cron',
            hour=23,
            minute=10,
            id="export_job",
            replace_existing=True
        )
