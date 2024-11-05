from aiogram import Router, types
from filters.admin import AdminFilter
    

# Создаем роутер для администраторов
admin_router = Router(name=__name__)


@admin_router.message(AdminFilter())
async def only_for_admins(message: types.Message):
    await message.reply("Only for admins!")


