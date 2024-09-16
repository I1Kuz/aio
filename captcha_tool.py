from captcha.image import ImageCaptcha
from random import choices
from string import ascii_uppercase, digits
from os import remove

# Указываем путь к шрифтам
image = ImageCaptcha(fonts=[r'artwork\OPIUM.TTF', r'artwork\OPIUM.TTF'])

def create_captcha(user_id: str):
    # Генерация случайного кода капчи
    captcha_text = ''.join(choices(ascii_uppercase + digits, k=4))
    
    # Путь для сохранения капчи (используем сырой строковый литерал для путей)
    captcha_path = rf'captchas\{user_id}.png'
    
    # Создание и запись изображения капчи
    image.write(captcha_text, captcha_path)
    print(f"Captcha created for user {user_id} with text: {captcha_text}")
    return captcha_path, captcha_text

def delete_captcha_file(user_id: str):
    # Путь для удаления файла капчи
    captcha_path = rf'captchas\{user_id}.png'
    
    # Удаление файла капчи
    try:
        remove(captcha_path)
        print(f"Captcha file for user {user_id} has been deleted.")
    except FileNotFoundError:
        print(f"Captcha file for user {user_id} not found.")


