FROM python:3.10.0-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt-get install -y build-essential \
  && apt-get install -y libpq-dev \
  && apt-get install -y gettext \
  && apt-get install tk --yes \
  && apt-get -y install netcat gcc postgresql \
  && apt-get install --no-install-recommends -y python3-gdal\
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

RUN pip3 install -r /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.dev.txt

COPY ./app /app
WORKDIR /app
EXPOSE 8000

COPY ./docker/dev/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./docker/dev/start.sh /start.sh
RUN chmod +x /start.sh


ARG DEV=false

ENTRYPOINT ["/entrypoint.sh"]


