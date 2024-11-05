from aiogram import BaseMiddleware, types, Bot
from aiogram.types import BufferedInputFile

from database.crud import is_captcha_solved
from database.database import session_scope
from services.captcha import gen_captcha, captcha_storage



class CaptchaMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot

    async def __call__(self, handler, event: types.Message, data):
        user_id = event.from_user.id

        with session_scope() as session:
            captcha_solved = is_captcha_solved(session, user_id)
            
            if not captcha_solved:
                captcha_bytes, captcha_text = gen_captcha()
                captcha_storage[user_id] = captcha_text
                
                captcha_image = BufferedInputFile(file=captcha_bytes, filename=f"captcha_{user_id}.png")
                await self.bot.send_photo(
                    chat_id=event.chat.id,
                    photo=captcha_image,
                    caption="Введите текст с изображения, чтобы пройти проверку."
                )
                return  
            
        return await handler(event, data)




