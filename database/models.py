from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, BigInteger
from .async_database import Base
from services.share_utils import utcnow_without_microsec

class User(Base):
    """
    main columns:
        user_id: Telegram user ID
        email: email lol
        username: username in Telegram(@username)
        first_name: user first name
        last_name: user last name, this may be missing
        is_bot: responsible for whether the user is a bot
    addition columns:
        verified: future
        banned_at: responsible for whether the user is a banned and when 
        created_at: date and time of record creation
        last_seen: date and time of last interaction
    setting and interactions data:
        preferences: future
        session_data: future
        activity_log: future
    """
    __tablename__ = 'telegram_users'

    user_id = Column(BigInteger, primary_key=True, )
    email = Column(String, nullable=True)
    username = Column(String(50), unique=True, nullable=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    is_bot = Column(Boolean, default=False)
    

    verified = Column(Boolean, default=False)
    banned_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=utcnow_without_microsec)
    deleted_at = Column(DateTime, nullable=True)
    last_seen = Column(DateTime, default=utcnow_without_microsec)

    preferences = Column(JSON, nullable=True)
    session_data = Column(JSON, nullable=True)
    activity_log = Column(JSON, nullable=True)

    def __repr__(self):
        return f"<TelegramUser(id={self.user_id}, username='{self.username}'"
