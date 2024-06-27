# Dev Dominic Minnich 2024
# scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import atexit
import subprocess

def backup_database():
    try:
        # Call the backup script
        subprocess.run(['python', 'backup_db.py'], check=True)
        print('Database backup completed successfully!')
    except subprocess.CalledProcessError as e:
        print(f'An error occurred during the backup: {e}')

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func=backup_database,
        trigger=IntervalTrigger(days=3),
        id='database_backup_job',
        name='Database Backup Job',
        replace_existing=True
    )
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
