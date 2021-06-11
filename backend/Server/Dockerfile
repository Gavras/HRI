FROM python:3.7

RUN pip install Flask gunicorn
RUN pip3 install psycopg2=2.8.6

COPY src/ app/
WORKDIR /app

ENV PORT 8002

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
