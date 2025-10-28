import asyncio
import os
import django
import subprocess

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from bot.main import bot_main

async def main():
    # Django serverni subprocess orqali ishga tushirish
    django_proc = subprocess.Popen(
        ["python", "manage.py", "runserver", "0.0.0.0:8000"]
    )

    try:
        # Botni asyncio-da ishga tushirish
        await bot_main()
    finally:
        django_proc.terminate()
        await django_proc.wait()

if __name__ == "__main__":
    asyncio.run(main())
