from os import getenv

ADMINS: list[str] = getenv('ADMINS').split(',')
BOT_TOKEN: str = getenv('BOT_TOKEN')
DB_URL: str = getenv('DB_URL')
NGROK_TUNNEL_URL: str = getenv('NGROK_TUNNEL_URL')
WEBHOOK_PATH: str = f"/{BOT_TOKEN}"
WEBHOOK_URL: str = NGROK_TUNNEL_URL + WEBHOOK_PATH
REDIS_HOST: str = getenv('REDIS_HOST')


