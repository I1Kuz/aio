from aiogram import Router, types, html
from aiogram.filters import Command, CommandStart
from database.crud import add_user
from filters.user import get_user_data
USER_HELP_TEXT = """    /help - памаги
                                 /top - пасмотреть топ prekolistov 
                                 \n /anek - палучить случайный анекдот или цитату
                                 \n или проста отправь мне prekol и если он мне понравится 
                                 то я иго вылажу в канал """
# Create router for users
user_router = Router(name=__name__)

@user_router.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    add_user(**get_user_data())
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@user_router.message(Command("help"))
async def user_help_handler(message: types.Message):
    await message.answer(USER_HELP_TEXT)
