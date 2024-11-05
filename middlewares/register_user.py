from __future__ import annotations
from typing import *
from typing import Coroutine
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
import redis.asyncio.client 
import time
import logging


class RegisterUserMiddleware(BaseMiddleware):
        def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject, data: redis.asyncio.client.Dict[str, redis.asyncio.client.Any]) -> Coroutine[Any, Any, Any]:
                return super().__call__(handler, event, data)