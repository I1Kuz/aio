from aiogram import Router, types, html
from aiogram.filters import Command, CommandStart
from database.async_crud import is_user_exists, add_user, update_user
from database.async_database import session_scope
from database.redis_cache import cache_user, get_all_users

USER_HELP_TEXT = """    /help - памаги
                                 /top - пасмотреть топ prekolistov 
                                 \n /anek - палучить случайный анекдот или цитату
                                 \n или проста отправь мне prekol и если он мне понравится 
                                 то я иго вылажу в канал """
# Create router for users
user_router = Router(name=__name__)


def get_user_data(message: types.Message):
    """
    Extracts user data from a Message object and returns it as a dictionary.
    
    :param message: Aiogram Message object containing user information.
    :return: Dictionary with user data.
    """
    return {
        "user_id": message.from_user.id,
        "username": message.from_user.username,
        "first_name": message.from_user.first_name,
        "last_name": message.from_user.last_name,
        "is_bot": message.from_user.is_bot,
        "last_seen": message.date.replace(microsecond=0), # add .isoformat() to put in redis
    }

@user_router.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")

@user_router.message(Command('register'))
async def register_handler(message: types.Message):
    """
    This handler receives messages with `/register` command and
    register user or update in DataBase 
    """
    async with session_scope() as session:
        data = get_user_data(message)

        if  await is_user_exists(session, message.from_user.id):

            await message.answer(f"Dear, {html.bold(message.from_user.full_name)}, you already have account!")
            await update_user(session, **data)
        else:
            
            await add_user(session, **data)
            await message.answer(f"Congratulation, {html.bold(message.from_user.full_name)}, your account registered!")

@user_router.message(Command('play'))
async def play_handler(message: types.Message):
    
@user_router.message(Command("help"))
async def user_help_handler(message: types.Message):
    await message.answer(USER_HELP_TEXT)
