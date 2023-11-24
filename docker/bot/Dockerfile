# syntax = docker/dockerfile:experimental
FROM python:3.11-alpine

RUN apk --no-cache add nano


RUN apk --no-cache add nano

WORKDIR /code

COPY ./docker/bot/requirements.txt .
COPY ./src/bot /code

RUN --mount=type=cache,target=/root/.cache/pip pip install wheel && pip install -r requirements.txt

CMD python -m main.py
