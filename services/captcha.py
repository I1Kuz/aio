from random import choices
from string import digits, ascii_letters
from captcha.image import ImageCaptcha
from io import BytesIO
import os


captcha_storage = {}

CAPTCHA_LENGTH = 4  



def gen_captcha():
    chars = ''.join(choices(digits + ascii_letters, k=CAPTCHA_LENGTH))
    
    font_path = os.path.join(os.path.dirname(__file__), '..', 'artwork', 'fonts')
    fonts = [os.path.join(font_path, font) for font in os.listdir(font_path)]
    
    captcha_image = ImageCaptcha(fonts=fonts)
    
    # Создаем изображение капчи и читаем его как байты
    captchaIO = BytesIO()
    captcha_image.write(chars, captchaIO)
    captchaIO.seek(0)  # Устанавливаем курсор в начало для чтения
    
    return captchaIO.read(), chars  # Возвращаем байты вместо BytesIO


