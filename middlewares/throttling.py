from __future__ import annotations
from typing import *
from aiogram import BaseMiddleware
from aiogram.types import Message
import redis.asyncio.client
import time
import logging
from database.async_crud import ban_user
from database.async_database import session_scope

def rate_limit(limit: int, key: str = None):
    """
    Decorator for configuring rate limit and key in different functions.
    """
    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)
        if key:
            setattr(func, 'throttling_key', key)
        return func
    return decorator

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, redis: redis.asyncio.client.Redis, limit=1.0, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        self.throttle_manager = ThrottleManager(redis=redis)
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        try:
            await self.on_process_event(event, data)
        except CancelHandler:
            return
        
        try:
            await self.check_forward(event)
        except CancelHandler:
            return


        try:
            result = await handler(event, data)
        except Exception as e:
            logging.exception(e)
            return
        return result

    async def on_process_event(self, event: Message, data: dict) -> Any:
        limit = getattr(data["handler"].callback, "throttling_rate_limit", self.rate_limit)
        key = getattr(data["handler"].callback, "throttling_key", f"{self.prefix}_message")

        try:
            await self.throttle_manager.throttle(key, rate=limit, user_id=event.from_user.id, chat_id=event.chat.id)
        except Throttled as t:
            await self.event_throttled(event, t)
            raise CancelHandler()

    async def event_throttled(self, event: Message, throttled: Throttled):
        delta = throttled.rate - throttled.delta
        if throttled.exceeded_count <= 2:
            await event.answer(f'Too many requests.\nTry again in {delta:.2f} seconds.')

    async def check_forward(self, event: Message) -> bool:
        if bool(event.forward_from) and event.text in '/start, /register, /stats, /play':
            await event.answer(f'Command message forwarded. Your account is banned.')

            async with session_scope() as session:
                await ban_user(session, event.from_user.id)
            raise CancelHandler()
        return False


class ThrottleManager:
    bucket_keys = ["RATE_LIMIT", "DELTA", "LAST_CALL", "EXCEEDED_COUNT"]

    def __init__(self, redis: redis.asyncio.client.Redis):
        self.redis = redis

    async def throttle(self, key: str, rate: float, user_id: int, chat_id: int):
        now = time.time()
        bucket_name = f'throttle_{key}_{user_id}_{chat_id}'
        
        data = await self.redis.hgetall(bucket_name)
        data = {k.decode(): float(v.decode()) for k, v in data.items()}

        called = data.get("LAST_CALL", now)
        delta = now - called
        result = delta >= rate or delta <= 0

        # Update data
        data["RATE_LIMIT"] = rate
        data["LAST_CALL"] = now
        data["DELTA"] = delta
        if not result:
            data["EXCEEDED_COUNT"] = data.get("EXCEEDED_COUNT", 0) + 1
        else:
            data["EXCEEDED_COUNT"] = 1

        await self.redis.hmset(bucket_name, data)

        if not result:
            raise Throttled(key=key, chat=chat_id, user=user_id, **data)
        
        return result

class Throttled(Exception):
    def __init__(self, **kwargs):
        self.key = kwargs.pop("key", '<None>')
        self.called_at = kwargs.pop("LAST_CALL", time.time())
        self.rate = kwargs.pop("RATE_LIMIT", None)
        self.exceeded_count = kwargs.pop("EXCEEDED_COUNT", 0)
        self.delta = kwargs.pop("DELTA", 0)
        self.user = kwargs.pop('user', None)
        self.chat = kwargs.pop('chat', None)

    def __str__(self):
        return f"Rate limit exceeded! (Limit: {self.rate} s, " \
               f"exceeded: {self.exceeded_count}, " \
               f"time delta: {round(self.delta, 3)} s)"

class CancelHandler(Exception):
    pass

