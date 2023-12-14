FROM python:3.9-alpine3.16

ENV PYTHONBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false

RUN python -m venv /py && \
    # Postgres dependencies
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
      build-base postgresql-dev musl-dev && \
    # Translations dependencies \
    apk add --no-cache gettext && \
    # GeoDjango dependencies
    apk add --no-cache --virtual .build-deps-edge \
      --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing \
      --repository http://dl-cdn.alpinelinux.org/alpine/edge/main \
      binutils geos proj gdal && \
     ln -s /usr/lib/libproj.so.15 /usr/lib/libproj.so && \
     ln -s /usr/lib/libgdal.so.20 /usr/lib/libgdal.so && \
     ln -s /usr/lib/libgeos_c.so.1 /usr/lib/libgeos_c.so && \
    # Upgrade pip
    /py/bin/pip install --upgrade pip && \
    # Install project requirements
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
      then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser --disabled-password --no-create-home django-user

ENV PATH="/py/bin:$PATH"

USER django-user
