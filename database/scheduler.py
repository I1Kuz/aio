from apscheduler.schedulers.background import BackgroundScheduler
from .sync import sync_redis_to_db  

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(sync_redis_to_db, 'interval', minutes=15)
    scheduler.start()