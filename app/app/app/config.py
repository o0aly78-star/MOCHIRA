import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
DB_PATH = os.getenv("DB_PATH", "data/mochira.db")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is missing. Set it in the server environment.")
