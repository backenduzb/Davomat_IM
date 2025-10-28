# Base image
FROM python:3.13-slim

# Workdir
WORKDIR /app

# Requirements
COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Bot code
COPY . .

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Bot token Railway secrets sifatida beriladi
ENV BOT_TOKEN=<YOUR_BOT_TOKEN>

# Run bot
CMD ["python", "-m", "bot.main"]
