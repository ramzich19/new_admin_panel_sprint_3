FROM python:3.10-alpine


WORKDIR /etl

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 and curl
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev \
    && apk --no-cache add curl

# install python dependencies
RUN pip install --upgrade pip
COPY requirements.txt /etl/
RUN pip install -r requirements.txt --no-cache-dir

COPY wait_to_start.sh /etl/

