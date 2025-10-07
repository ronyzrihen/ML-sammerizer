FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY healthcheck.py /app/
RUN chmod +x /app/healthcheck.py
EXPOSE 8000

