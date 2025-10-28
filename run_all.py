import asyncio
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.core.management import call_command
from bot.main import bot_main

async def main():
    # Django serverni asyncio’da fon ishga tushirish
    loop = asyncio.get_running_loop()
    loop.run_in_executor(None, lambda: call_command("runserver", "0.0.0.0:8000"))

    # Aiogram botni ishga tushirish
    await bot_main()

if __name__ == "__main__":
    asyncio.run(main())
