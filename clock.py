from apscheduler.schedulers.background import BlockingScheduler
from utilities import covid19

scheduler = BlockingScheduler()
#scheduler.add_job(covid19.update_data, 'cron', hour=16, minute=10)  # Updating COVID Data
scheduler.add_job(covid19.update_data, 'interval', seconds=60)  # Updating COVID Data

scheduler.start()
