import redis # type: ignore
import json


# Подключение к Redis (замените параметры на ваши, если нужно)
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Сохранение пользователя в Redis
def cache_user_data(user_id, user_data):
    redis_client.set(f"user:{user_id}", json.dumps(user_data))

# Получение всех пользователей из Redis
def get_all_cached_users():
    keys = redis_client.keys("user:*")
    users = []
    for key in keys:
        user_data = redis_client.get(key)
        users.append(json.loads(user_data))
    return users

# Очистка кэша после синхронизации
def clear_cache():
    redis_client.flushdb()
