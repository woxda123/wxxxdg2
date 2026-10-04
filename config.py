import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_TOKEN_HERE")
DB_PATH = os.getenv("DB_PATH", "wox_mafia.db")
DEFAULT_LANG = "ru"
SUPPORTED_LANGS = ["ru","en","uk","be","kk","uz","de","fr","es","it","pt","tr","pl","cs","sk","hu","ro","bg","sr","hr","nl","sv","no","da","fi","el"]
BOT_USERNAME = os.getenv("BOT_USERNAME", "Wox_Mafiabot")
