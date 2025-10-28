#!/bin/sh

python3 manage.py makemigrations --no-input
python3 manage.py migrate --no-input

python3 telegram_bot.py &
gunicorn config.wsgi --bind 0.0.0.0:8000 --workers 4
