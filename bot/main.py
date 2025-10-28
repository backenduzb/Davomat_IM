import asyncio
import logging
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup() 

from aiogram import Bot, Dispatcher
from bot.config.settings import BOT_TOKEN, DEFAULT_PROPERTIES
from bot.handlers import start
from bot.handlers.teacher import (
    not_reason,
    reason,
)
from bot.handlers.admin import (
    class_,
    no_reason,
    reasona
)
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    "bot.log", maxBytes=200*1024*1024, backupCount=3, encoding="utf-8"
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
    handlers=[
        handler,
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

async def bot_main():
    bot = Bot(token=BOT_TOKEN, default=DEFAULT_PROPERTIES)
    dp = Dispatcher()
    
    dp.include_routers(
        start.router,
        class_.router,
        reasona.router,
        no_reason.router,
        reason.router,
        not_reason.router,
    )  

    logger.error("---------------------------------------------------------------------------------------------------------")    
    logger.info("🤖 Bot ishga tushmoqda...")

    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Bot ishlashida xatolik: {e}")
    finally:
        await bot.session.close()
        
        logger.info("🛑 Bot to‘xtatildi.")
        
        logger.error("---------------------------------------------------------------------------------------------------------")


if __name__ == "__main__":
    asyncio.run(bot_main())
