from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, BigInteger
from .async_database import Base
from services.share_utils import utcnow_without_microsec

class TelegramUser(Base):
    """
    main columns:
        user_id: Telegram user ID, BigInteger because its 64bit number.
        username: username in Telegram(@username)
        first_name: user first name
        last_name: user last name, this may be missing
        language_code: IETF language tag <https://en.wikipedia.org/wiki/IETF_language_tag>_ of the user's language
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

    user_id = Column(BigInteger, primary_key=True)  
    username = Column(String(50), unique=True, default='Unknown')  
    first_name = Column(String(100), default='Unknown')  
    last_name = Column(String(100), default='Unknown')  
    language_code = Column(String(10), default='Unknown')
    is_bot = Column(Boolean, default=False)

    verified = Column(Boolean, default=False)
    banned_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=utcnow_without_microsec)  
    last_seen = Column(DateTime, default=utcnow_without_microsec)

    preferences = Column(JSON, nullable=True)  
    session_data = Column(JSON, nullable=True)  
    activity_log = Column(JSON, nullable=True)  

    def __repr__(self):
        return f"<TelegramUser(id={self.user_id}, username='{self.username}', language_code='{self.language_code}')>"
