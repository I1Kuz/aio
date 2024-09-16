import asyncio
import logging
import sys
from os import getenv

import crud
import anek
import captcha_tool

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile



# Bot token and ADMIN ID
TOKEN = getenv("TOKEN")
ADMIN_ID = getenv("ADMIN_ID") 

HELP_TEXT = """    /help - памаги
                                 /top - пасмотреть топ prekolistov 
                                 \n /anek - палучить случайный анекдот или цитату
                                 \n или проста отправь мне prekol и если он мне понравится 
                                 то я иго вылажу в канал """

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)

# Временное хранилище для текстов капчи
user_captcha_data = {}



@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    user_id = message.from_user.id

    if not crud.user_exists(user_id):
        # Создаем капчу для нового пользователя
        captcha_path, captcha_text = captcha_tool.create_captcha(user_id)
        user_captcha_data[user_id] = captcha_text
        
        # Отправляем капчу пользователю
        await bot.send_photo(chat_id=user_id, photo=FSInputFile(captcha_path), caption="Пожалуйста, введите текст с картинки для завершения регистрации.")
        captcha_tool.delete_captcha_file(user_id)  # Удаляем файл капчи после отправки
    else:
        await message.answer("Вы уже зарегистрированы. Отправьте мне prekol, чтобы предложить его для канала.")

@dp.message(Command('help'))
async def helpe(message: Message):
    await message.answer(HELP_TEXT)
    
@dp.message(Command("top"))
async def top(message: Message):
    top_users = crud.get_top_10_users()

    if top_users:
        response_text = "Топ 10 пользователей по количеству отправленных prekols:\n\n"
        for index, user in enumerate(top_users, start=1):
            response_text += f"{index}. {user.username} — {user.memes_sent} prekols\n"
    else:
        response_text = "Пока нет активных пользователей."

    await message.answer(response_text)

@dp.message(Command('anek'))
async def anek_hendler(message: Message):
    await message.answer(await anek.get_anekdot())
# Обработчик для приема фото, видео и текста
@dp.message()
async def handle_meme(message: Message):
    if not await check_captcha(message):  
        return

    user_id = message.from_user.id

    # Проверяем, отправил ли пользователь фото, видео или текст
    if message.photo or message.video:
        # Если это фото
        if message.photo:
            media_id = message.photo[-1].file_id
        # Если это видео
        elif message.video:
            media_id = message.video.file_id

        caption = message.caption if message.caption else "no caption sisi blal"

        try:
            # Отправляем фото или видео админу в анал
            await bot.send_photo(ADMIN_ID, photo=media_id, caption=f"by {message.from_user.full_name}: {caption}") if message.photo else \
                await bot.send_video(ADMIN_ID, video=media_id, caption=f"by {message.from_user.full_name}: {caption}")
            
            await message.answer("Ваш prekol отправлен на рассмотрение.")
            crud.increment_memes_sent(user_id)
        except Exception as e:
            await message.answer("Произошла ошибка при отправке prekola.")
            logging.error(f"Ошибка при пересылке prekola: {e}")

    elif message.text:
        # Если это текст
        text_content = message.text.strip()

        try:
            # Отправляем текст админу
            await bot.send_message(ADMIN_ID, text=f"by {message.from_user.full_name}: {text_content}")
            await message.answer("Ваш текст отправлен на рассмотрение.")
            crud.increment_memes_sent(user_id)
        except Exception as e:
            await message.answer("Произошла ошибка при отправке текста.")
            logging.error(f"Ошибка при пересылке текста: {e}")
    
    else:
        await message.answer("Пожалуйста, отправьте фото, видео, текст, чтобы предложить prekol, или напишите /help для дополнительных инструкций.")

async def check_captcha(message: Message):
    user_id = message.from_user.id
    # Проверяем, если пользователь в процессе прохождения капчи
    if user_id in user_captcha_data:
        entered_text = message.text.strip().upper()  # Приводим к верхнему регистру для сравнения с капчей
        correct_captcha = user_captcha_data[user_id]

        if entered_text == correct_captcha:
            await message.answer("Капча успешно пройдена!")
            await message.answer(HELP_TEXT)
            
            del user_captcha_data[user_id]
            crud.add_user(user_id, message.from_user.full_name)
        else:
            await message.answer("Неправильный текст капчи. Попробуйте снова.")
        return False
    return True


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
