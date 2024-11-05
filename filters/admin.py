from aiogram.filters import Filter
from aiogram import types
from core.config import ADMINS

class AdminFilter(Filter):
    key = "AdminFilter"

    async def __call__(self, message: types.Message):
        return message.from_user.id in ADMINS