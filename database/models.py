from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, BigInteger
from .database import Base
from services.share_utils import utcnow_without_microsec

class TelegramUser(Base):
    __tablename__ = 'telegram_users'

    # Основные данные пользователя
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)  # Telegram ID пользователя
    chat_id = Column(BigInteger, unique=True, nullable=False)  # Chat ID
    username = Column(String(50), unique=True)  # Никнейм пользователя в Telegram
    first_name = Column(String(100))  # Имя пользователя
    last_name = Column(String(100))  # Фамилия пользователя
    language_code = Column(String(10))  # Код языка пользователя (например, 'en', 'ru')

    # Дополнительные данные
    is_bot = Column(Boolean, default=False)  # Является ли пользователь ботом
    verified = Column(Boolean, default=False)  # Верифицирован ли пользователь
    ban = Column(Boolean, default=False)  # Забанен ли пользователь
    banned_at = Column(DateTime)
    created_at = Column(DateTime, default=utcnow_without_microsec)  # Дата и время создания записи
    last_seen = Column(DateTime, default=utcnow_without_microsec)  # Дата и время последнего взаимодействия с ботом

    # Настройки и данные взаимодействия
    preferences = Column(JSON)  # Настройки пользователя
    session_data = Column(JSON)  # Данные сессии пользователя
    activity_log = Column(JSON)  # Лог активности пользователя

    def __repr__(self):
        return f"<TelegramUser(id={self.user_id}, username='{self.username}', language_code='{self.language_code}')>"
