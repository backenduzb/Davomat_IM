import fcntl
import os
import tempfile

from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone

from .jobs import export_data

scheduler = BackgroundScheduler(timezone=str(timezone.get_current_timezone()))
_lock_file = None


def _acquire_lock():
    global _lock_file

    if _lock_file:
        return True

    lock_path = os.path.join(tempfile.gettempdir(), "davomat_apscheduler.lock")
    lock_file = open(lock_path, "w")

    try:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        lock_file.close()
        return False

    _lock_file = lock_file
    return True


def start():
    global scheduler

    if not _acquire_lock():
        return

    if not scheduler.running:
        scheduler.start()

    if not scheduler.get_job("export_job"):
        scheduler.add_job(
            export_data,
            "cron",
            hour=23,
            minute=15,
            id="export_job",
            replace_existing=True,
        )
