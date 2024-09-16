import requests
import random


async def get_anekdot():
    url = f'http://rzhunemogu.ru/RandJSON.aspx?CType={random.randint(1,15)}'
    response = requests.get(url)
    
    # Удаляем ненужные символы и пробелы
    response_text = response.text.strip()
    return response_text[12:-3]
    






