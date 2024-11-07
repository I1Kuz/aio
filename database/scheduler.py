from apscheduler.schedulers.background import BackgroundScheduler
from .sync_dbs import sync_redis_to_db  

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(sync_redis_to_db, 'interval', seconds=15)
    scheduler.start()
