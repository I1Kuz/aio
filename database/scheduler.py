from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .sync_dbs import sync_redis_to_db  

async def run_async_job():
    await sync_redis_to_db()  # Асинхронный вызов функции

def start_scheduler():
    scheduler = AsyncIOScheduler()
    # Используем add_job для асинхронной функции
    scheduler.add_job(run_async_job, 'interval', seconds=60)
    scheduler.start()
