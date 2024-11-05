from aiogram.filters import Filter
from aiogram import types
from database.crud import is_user_exists, add_user
from database.database import session_scope

def get_user_data(message: types.Message):
    return {"user_id":message.from_user.id, 
     "chat_id":message.chat.id,
     "username":message.from_user.username,
     "first_name":message.from_user.first_name,
     "last_name":message.from_user.last_name,
     "language_code":message.from_user.language_code,
     "is_bot":message.from_user.is_bot}
    # TODO add all data to colums in db
        
    

class UserFilter(Filter):
    key = "UserFilter"

    async def __call__(self, message: types.Message):
        with session_scope() as session:
            if  not is_user_exists(session=session,
                                  user_id=message.from_user.id):
                add_user(session=session, )