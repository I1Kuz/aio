from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .sync_dbs import sync_redis_to_db  

def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(sync_redis_to_db, 'interval', seconds=60)
    scheduler.start()

