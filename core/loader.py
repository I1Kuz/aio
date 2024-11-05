import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from .config import BOT_TOKEN


# Initialize Bot instance with default bot properties which will be passed to all API calls
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML), 
    proxy = 'https://185.65.105.56:3128'
    )

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    
