# Base image
FROM python:3.13-slim

# Workdir
WORKDIR /app

# Requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App code (faqat Django loyihasi)
COPY manage.py .
COPY config/ config/
COPY main/ main/
COPY students/ students/
COPY teachers/ teachers/
COPY static/ static/
COPY upload/ upload/

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Port for Railway
EXPOSE 8000

# Run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
