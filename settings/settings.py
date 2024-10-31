import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    TOKEN: str = str(os.getenv('BOT_TOKEN'))
    DB_LITE: str = str(os.getenv('DB_LITE'))


