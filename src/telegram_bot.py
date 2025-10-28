import django
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from bot.config.settings import (
    BOT_TOKEN,
    DEFAULT_PROPERTIES,
    BASE_WEBHOOK_URL,
    WEBHOOK_PATH,
    WEBHOOK_SECRET,
    WEB_SERVER_HOST,
    WEB_SERVER_PORT
)
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
import sys
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}", secret_token=WEBHOOK_SECRET)


def main() -> None:
    dp = Dispatcher()
    dp.include_routers(
        start.router,
        class_.router,
        reasona.router,
        no_reason.router,
        reason.router,
        not_reason.router,
    )

    dp.startup.register(on_startup)

    bot = Bot(token=BOT_TOKEN, default=DEFAULT_PROPERTIES)

    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET,
    )

    webhook_requests_handler.register(app, path=WEBHOOK_PATH)

    setup_application(app, dp, bot=bot)
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()
