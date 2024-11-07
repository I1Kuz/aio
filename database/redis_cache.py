import redis.asyncio as aioredis  
import json
import logging
from core.config import REDIS_HOST


redis_client = aioredis.Redis(host=REDIS_HOST)
# redis_client = aioredis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


async def redis_ping():
    try:
        await redis_client.ping()
        logging.info("Connected to Redis")
    except Exception as e:
        logging.critical(f"Could not connect to Redis: {e}")


async def cache_user_data(user_id: int, **user_data):
    await redis_client.set(f"user:{user_id}", json.dumps(user_data))


async def get_all_cached_users():
    keys = await redis_client.keys("user:*")
    users = []
    for key in keys:
        user_data = await redis_client.get(key)
        users.append(json.loads(user_data))
    return users


async def clear_cache():
    await redis_client.flushdb()



