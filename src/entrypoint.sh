
python3 manage.py makemigrations --no-input
python3 manage.py migrate --no-input

python3 manage.py createadmin
python3 manage.py collectstatic --no-input

python3 manage.py runbot &
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4