from .async_crud import set_user
from .async_database import session_scope
from .redis_cache import get_all_users, delete_user_from_cache
from datetime import datetime

async def sync_redis_to_db():
    cached_users = await get_all_users()
    async with session_scope() as session:
        for user in cached_users:

            user['last_seen'] = datetime.fromisoformat(user['last_seen'])
            
            # Move the user data to the database
            await set_user(session=session, **user)
            
            # Remove user from Redis cache after saving to the database
            await delete_user_from_cache(user_id=user["user_id"])
