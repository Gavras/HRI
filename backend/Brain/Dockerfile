FROM python:2.7

COPY src/ app/
WORKDIR /app

ENV PORT 8001

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
