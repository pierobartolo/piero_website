from apscheduler.schedulers.background import BackgroundScheduler
from utilities import covid19

scheduler = BackgroundScheduler(daemon=True)
#scheduler.add_job(covid19.update_data, 'cron', hour=16, minute=10)  # Updating COVID Data
scheduler.add_job(covid19.update_data, 'interval', seconds=60)  # Updating COVID Data
scheduler.start()
