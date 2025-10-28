FROM python:3.13-alpine3.21

WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /app

EXPOSE 8000

CMD ["gunicorn", "config.wsgi", "--bind", "0.0.0.0:8000", "--workers", "4"]
