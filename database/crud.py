from .models import TelegramUser
from sqlalchemy.orm import Session
from sqlalchemy import exists


def add_user(session: Session, user_id: int, chat_id: int, username: str, 
             first_name: str = None, last_name: str = None, language_code: str = None, 
             is_bot: bool = False, verified: bool = False, ban: bool = False):
    
    if not is_user_exists(session, user_id):
        new_user = TelegramUser(
            user_id=user_id,
            chat_id=chat_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            language_code=language_code,
            is_bot=is_bot,
            verified=verified,
            ban=ban,
        )
        session.add(new_user)
        print(new_user.__dict__)
        # print(f"Added user {username} with ID {user_id}.")
    else:
        print("User already exists.")

def update_user(session: Session, user_id: int, **kwargs):
    user = session.query(TelegramUser).filter_by(user_id=user_id).first()
    
    if user:
        # update fields that passed in kwars only  
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        session.add(user)
        print(f"Updated user {user_id} with {kwargs}")
    else:
        print("User not found.")

def get_user_banned(session: Session, user_id: int):
    user = session.query(TelegramUser).filter_by(user_id=user_id).first()
    return user.is_banned if user else None

def is_user_exists(session: Session, user_id: int) -> bool:
    return session.query(exists().where(TelegramUser.user_id == user_id)).scalar()





