from .crud import add_user
from .database import session_scope
from .redis_cache import get_all_cached_users, clear_cache

def sync_redis_to_db():
    cached_users = get_all_cached_users()
    with session_scope() as session:
        for user_data in cached_users:
            # Transform the data into the required format and add it to the database
            add_user(
                session=session,
                user_id=user_data['telegram_id'],
                username=user_data['username'],
                is_banned=user_data.get('is_banned', False),
                chat_id=user_data['chat_id']
            )
    clear_cache()  # Clear cache after move data to database

def sync_db_request_to_sync():
    ...