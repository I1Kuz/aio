import logging
from aiogram import Bot

from core.config import ADMINS


async def on_startup_notify(bot: Bot):
    """Notify admins about successful start"""
    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=admin, text="Bot turned on.")
        except Exception as e:
            logging.exception(e)


async def on_shutdown_notify(bot: Bot):
    """Notify admins about successful stop"""
    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=admin, text="Bot shutted down.")
        except Exception as e:
            logging.exception(e)