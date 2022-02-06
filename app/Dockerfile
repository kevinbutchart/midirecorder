FROM python:3.7-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install –no-install-recommends -yy build-essential libasound2-dev librtmidi-dev && \
    python3 -m pip install --upgrade pip &&\
    python3 -m pip install -r requirements.txt
COPY . .
