from aiogram import Router, types, html
from aiogram.filters import Command, CommandStart
from database.async_crud import set_user
from database.async_database import session_scope
from database.redis_cache import cache_user_data, get_all_users

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
        "language_code": message.from_user.language_code,
        "is_bot": message.from_user.is_bot,
        "last_seen": message.date.isoformat(),
    }

@user_router.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    message.reply('Hi there, ')
    # async with session_scope() as session:
    #     data = get_user_data(message)
    #     await set_user(session, **data)

    data = get_user_data(message)
    await cache_user_data(**data)

    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")
    print(await get_all_users())

@user_router.message(Command('register'))
    
@user_router.message(Command("help"))
async def user_help_handler(message: types.Message):
    await message.answer(USER_HELP_TEXT)
