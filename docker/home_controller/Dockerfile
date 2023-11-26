# syntax = docker/dockerfile:experimental
FROM python:3.11-alpine

RUN pip install --upgrade pip
RUN apk --no-cache add gcc musl-dev linux-headers libffi-dev nano

WORKDIR /code

COPY ./docker/home_controller/requirements.txt .
COPY ./src/home_controller /code

RUN pip install --no-cache-dir -r requirements.txt

CMD python -m main.py
