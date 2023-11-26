# syntax = docker/dockerfile:experimental
FROM python:3.11-alpine

RUN apk --no-cache add nano gcc musl-dev alsa-lib-dev portaudio-dev

WORKDIR /code

COPY ./docker/assistant/requirements.txt .
COPY ./src/assistant /code

RUN --mount=type=cache,target=/root/.cache/pip pip install wheel && pip install -r requirements.txt

CMD python -m main.py
