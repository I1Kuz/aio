from create_base import *

# Настройка сессии для взаимодействия с БД
Session = sessionmaker(bind=engine)
session = Session()

# Функция для добавления пользователя
def add_user(user_id: int, username: str, is_banned=False):
    if not user_exists(user_id):
        new_user = User(user_id=user_id, username=username, is_banned=is_banned)
        session.add(new_user)
        session.commit()
    else:
        print("User already exists.")

# Функция для изменения статуса блокировки
def ban(user_id: int, ban=True):
    user_to_ban = session.query(User).filter_by(user_id=user_id).first()
    if user_to_ban:
        user_to_ban.is_banned = ban  # Устанавливаем переданное значение параметра ban
        session.commit()
        print(f"User {user_id} {'banned' if ban else 'unbanned'}.")
    else:
        print("User not found.")

# Функция для проверки статуса блокировки
def is_user_banned(user_id: int):
    user = session.query(User).filter_by(user_id=user_id).first()
    if user:
        return user.is_banned
    else:
        print("User not found.")
        return None

# Функция для проверки, существует ли пользователь
def user_exists(user_id: int) -> bool:
    # Проверяем, существует ли пользователь с данным user_id
    user = session.query(User).filter_by(user_id=user_id).first()
    return user is not None

def increment_memes_sent(user_id: int):
    user = session.query(User).filter_by(user_id=user_id).first()
    user.memes_sent += 1
    session.commit()

def get_top_10_users(limit = 10):
    top_users = session.query(User).order_by(User.memes_sent.desc()).limit(limit).all()
    
    return top_users

# Функция для удаления пользователя
def delete_user(user_id: int):
    user = session.query(User).filter_by(user_id=user_id).first()
    if user:
        session.delete(user)
        session.commit()
        print(f"User {user_id} deleted.")
    else:
        print("User not found.")
