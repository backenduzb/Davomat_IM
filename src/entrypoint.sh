#!/bin/sh

python3 manage.py makemigrations --no-input
python3 manage.py migrate --no-input

echo "admin123\nadmin123\n" | python3 manage.py createsuperuser --username admin --email admin@example.com

python3 telegram_bot.py &
gunicorn config.wsgi --bind 0.0.0.0:8000 --workers 4
