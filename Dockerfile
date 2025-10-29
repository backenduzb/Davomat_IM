FROM python:3.13-alpine3.21

WORKDIR /app

RUN apk add --no-cache build-base postgresql-dev musl-dev zlib-dev jpeg-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /app/src
COPY entrypoint.sh /app/entrypoint.sh

RUN python /app/src/manage.py collectstatic --noinput || true

EXPOSE 8000

ENTRYPOINT ["sh", "/app/src/entrypoint.sh"]
