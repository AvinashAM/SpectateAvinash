FROM python:3.12.4-slim-bookworm

WORKDIR  /app

RUN set -ex \
    && apt update \
    && apt install -y \
        curl \
        bash \
    && pip install -U pip

COPY requirements.txt /app/

RUN pip install -r requirements.txt
