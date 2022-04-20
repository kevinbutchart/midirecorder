FROM python:3.7-slim-buster as compile-image
ENV PATH=/root/.local/bin:$PATH
WORKDIR /root
COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -yy --no-install-recommends build-essential librtmidi-dev
RUN python3 -m pip install --upgrade pip &&\
    python3 -m pip install --user -r requirements.txt

FROM python:3.7-slim-buster as runtime-image
COPY --from=compile-image /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
RUN apt-get update && apt-get install -yy --no-install-recommends libasound2 librtmidi4 &&\
    rm -rf /var/lib/apt/lists/*

FROM runtime-image
WORKDIR /app
COPY . .
ENV PATH=/root/.local/bin:/app/bin:$PATH
