from sqlalchemy import create_engine, Column, Integer, Boolean, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Создание движка базы данных (здесь SQLite, можно использовать другие СУБД)
engine = create_engine('sqlite:///users.db', echo=True)


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String, default='')
    memes_sent = Column(Integer, default=0)
    is_banned = Column(Boolean, default=False)  



Base.metadata.create_all(engine)
