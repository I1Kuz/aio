from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists
from .models import TelegramUser


async def _add_user(session: AsyncSession, user_id: int, **user_data):
    """Add a new user to the database if they don't already exist."""
    new_user = TelegramUser(
        user_id=user_id, **user_data
    )
    session.add(new_user)
    

async def _update_user(session: AsyncSession, user_id: int, **user_data):
    """Update an existing user with new values for the fields provided in kwargs."""
    user = await session.execute(select(TelegramUser).filter_by(user_id=user_id))
    user = user.scalar_one()
    
    for key, value in user_data.items():
        if hasattr(user, key):
            setattr(user, key, value)


async def is_user_exists(session:AsyncSession, user_id: int):
    """Check is user exists"""
    user_exists = await session.execute(
        select(exists().where(TelegramUser.user_id == user_id))
    )
    user_exists = user_exists.scalar()

    return bool(user_exists)

async def set_user(session: AsyncSession, user_id: int, **user_data):
    """Check if the user exists. If they do, update their information. Otherwise, add them."""


    if await is_user_exists(session, user_id):
        # Fetch the user and update their details
        await _update_user(session, user_id, **user_data)
    else:
        # Add a new user if they do not exist
        await _add_user(session, user_id, **user_data)
