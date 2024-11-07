from .models import TelegramUser # type: ignore
from sqlalchemy.orm import Session
from sqlalchemy import exists


def _add_user(session: Session, user_id: int, username: str, 
              first_name: str = None, last_name: str = None, language_code: str = None, 
              is_bot: bool = False, verified: bool = False, ban: bool = False):
    new_user = TelegramUser(
        user_id=user_id,
        username=username,
        first_name=first_name,
        last_name=last_name,
        language_code=language_code,
        is_bot=is_bot,
        verified=verified,
        ban=ban
    )
    session.add(new_user)


def _update_user(session: Session, user_id: TelegramUser, **kwargs):
    # Update only the fields passed in kwargs
    for key, value in kwargs.items():
        if hasattr(user_id, key):
            setattr(user_id, key, value)
    session.add(user_id)


def set_user(session: Session, user_id: int, **kwargs):
    # Check if the user exists in the database
    user_exists = session.query(exists().where(TelegramUser.user_id == user_id)).scalar()
    
    if user_exists:
        # If user exists, fetch and update
        user = session.query(TelegramUser).filter_by(user_id=user_id).first()
        _update_user(session=session, user_id=user, **kwargs)
    else:
        # If user does not exist, add a new one
        _add_user(session=session, user_id=user_id **kwargs)
