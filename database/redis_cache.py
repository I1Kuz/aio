import redis.asyncio as aioredis  
import json
import logging
from core.config import REDIS_HOST

# Initialize the Redis client
redis_client = aioredis.Redis(host=REDIS_HOST)

async def redis_ping():
    """Ping Redis to ensure connection is active."""
    try:
        await redis_client.ping()
        logging.info("Connected to Redis")
    except Exception as e:
        logging.critical(f"Could not connect to Redis: {e}")


async def cache_user(**user_data: dict):
    """
    Caches user data in Redis by serializing it to JSON format.
    
    :param user_id: Unique identifier for the user.
    :param user_data: Dictionary containing user data.
    """
    await redis_client.set(f"user:{user_data['user_id']}", json.dumps(user_data))
    logging.info(f'user ceched: {user_data['user_id']}')


async def get_all_users():
    """
    Retrieves all user data from Redis, deserializing from JSON format.
    
    :return: List of user data dictionaries.
    """
    keys = await redis_client.keys("user:*")
    users = []
    for key in keys:
        user_data = await redis_client.get(key)
        users.append(json.loads(user_data))

    return users


async def get_user():
    ...


async def delete_user_from_cache(user_id: int):
    """
    Deletes a specific user's data from Redis based on user_id.
    
    :param user_id: The unique identifier for the user to delete from cache.
    """
    await redis_client.delete(f"user:{user_id}")


async def clear_cache():
    """Flushes all data from the Redis database."""
    await redis_client.flushdb()


