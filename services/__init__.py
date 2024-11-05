from aiogram import Dispatcher
from aiogram import types, Bot
from handlers import routers_list

# Set routers in Dispatcher
async def set_routers(dp: Dispatcher):
    for router in routers_list:
        dp.include_router(router)


# Set bot commands
async def set_default_commands(bot: Bot):
    def get_commands_de():
        commands = [
            types.BotCommand(command="/start", description="Bot starten"),
            types.BotCommand(command="/help", description="Helfen"),
        ]
        return commands


    def get_commands_ru():
        commands = [
            types.BotCommand(command="/start", description="Запустить бота"),
            types.BotCommand(command="/help", description="Помощь"),
        ]
        return commands


    def get_commands_en():
        commands = [
            types.BotCommand(command="/start", description="Start the bot"),
            types.BotCommand(command="/help", description="Help"),
        ]
        return commands
    await bot.set_my_commands(get_commands_de(), scope=types.BotCommandScopeAllPrivateChats(), language_code="de")
    await bot.set_my_commands(get_commands_ru(), scope=types.BotCommandScopeAllPrivateChats(), language_code="ru")
    await bot.set_my_commands(get_commands_en(), scope=types.BotCommandScopeAllPrivateChats(), language_code="en")

