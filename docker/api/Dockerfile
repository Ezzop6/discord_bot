FROM alpine:3.18

RUN apk add --no-cache python3 py3-pip
RUN pip install --upgrade pip

RUN apk --no-cache add nano

COPY ./docker/api/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /code

COPY ./src/api /code


CMD python -m main.py
