from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = "-1003013595617"
DEFAULT_PROPERTIES = DefaultBotProperties(
    parse_mode="HTML"
)

WEB_SERVER_HOST = "0.0.0.0"
WEB_SERVER_PORT = 8080
WEBHOOK_PATH = "/webhook"
WEBHOOK_SECRET = os.getenv("BOT_WEBHOOK_SECRET")
BASE_WEBHOOK_URL = os.getenv("BOT_BASE_URL")
