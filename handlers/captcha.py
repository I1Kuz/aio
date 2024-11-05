from aiogram import Router, types
from database.database import session_scope
from database.crud import set_captcha_status
from services.captcha import captcha_storage

captcha_router = Router(name=__name__)


@captcha_router.message()
async def check_captcha(message: types.Message):
    user_id = message.from_user.id
    user_input = message.text.strip()

    if user_id in captcha_storage:
        # Проверяем текст капчи
        if user_input == captcha_storage[user_id]:
            await message.reply("Капча успешно пройдена!")
            
            with session_scope() as session:
                set_captcha_status(session, user_id, True)
            
            del captcha_storage[user_id]
        
        else:
            await message.reply("Неверный текст капчи. Попробуйте снова.")
    else:
        await message.reply("Капча уже пройдена или не требуется.")