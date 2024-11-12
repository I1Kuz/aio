from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists, delete, update
from sqlalchemy.exc import NoResultFound, IntegrityError
from .models import TelegramUser
from ..services.share_utils import utcnow_without_microsec

async def add_user(session: AsyncSession, user_id: int, **user_data): # use set_user instead 
    """Add a new user to the database if they don't already exist."""
    new_user = TelegramUser(user_id=user_id, **user_data)
    session.add(new_user)

async def get_user(session: AsyncSession, user_id: int):
    """Retrieve a user by user_id."""
    try:
        result = await session.execute(select(TelegramUser).filter_by(user_id=user_id))
        return result.scalar_one()
    except NoResultFound:
        return None  

async def update_user(session: AsyncSession, user_id: int, **user_data):

    if 'user_id' in user_data:
        raise IntegrityError(None, None, f"Cannot modify immutable column 'user_id'")
    
    await session.execute(update(TelegramUser).where(TelegramUser.user_id == user_id).values(**user_data))
    
async def is_user_exists(session: AsyncSession, user_id: int):
    """Check if a user exists."""
    result = await session.execute(select(exists().where(TelegramUser.user_id == user_id)))
    return bool(result.scalar())

async def soft_delete_user(session: AsyncSession, user_id: int):
    await session.execute(update(TelegramUser).where(TelegramUser.user_id == user_id).values(deleted_at=utcnow_without_microsec()))
    
async def delete_user(session: AsyncSession, user_id: int):
    """Delete a user by user_id."""
    await session.execute(delete(TelegramUser).where(TelegramUser.user_id == user_id))

async def ban_user(session: AsyncSession, user_id: int):
    """Ban a user by setting the banned_at field."""
    await session.execute(update(TelegramUser).where(TelegramUser.user_id == user_id).values(banned_at=utcnow_without_microsec()))

async def set_user(session: AsyncSession, user_id: int, **user_data):
    """Check if the user exists; if they do, update, otherwise add them."""
    if await is_user_exists(session, user_id):
        await update_user(session, user_id, **user_data)
    else:
        await add_user(session, user_id, **user_data)

async def get_all_users(session: AsyncSession):
    """Retrieve all users."""
    result = await session.execute(select(TelegramUser))
    return result.scalars().all()
