# pull official base image
FROM python:3.13.0-slim-bookworm

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt install -y netcat-openbsd \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # Additional dependencies
  && apt-get install -y git procps pkg-config cmake \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# install dependencies
# RUN pip install --upgrade pip
COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

# copy entrypoint
COPY ./bphis/entrypoint.sh /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./bphis/start.sh /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./bphis/start-flask.sh /start-flask
RUN sed -i 's/\r$//g' /start-flask
RUN chmod +x /start-flask

COPY ./bphis/celery/celery-worker.sh /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./bphis/celery/celery-beat.sh /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

COPY ./bphis/celery/celery-flower.sh /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower

# run entrypoint
WORKDIR /app
ENTRYPOINT ["/entrypoint"]
