# syntax=docker/dockerfile:1
FROM python:3.8.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN set -ex; \
    apt-get update; \
    apt-get install -y sqlite3; \
    apt-get install -y --no-install-recommends \
        nano;
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
WORKDIR /app
