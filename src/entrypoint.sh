#!/bin/sh

python3 telegram_bot.py &
gunicorn config.wsgi --bind 0.0.0.0:8000 --workers 4
