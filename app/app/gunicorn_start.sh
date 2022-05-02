#!/bin/bash
#source env/bin/activate
export PATH=$HOME/.local/bin:$PATH
./gen_certs_if_needed.sh
exec gunicorn -w 1 --threads 4 -k uvicorn.workers.UvicornWorker --proxy-protocol --certfile=/data/pianorecorder.pem --keyfile=/data/pianorecorder.key main:app -b :8443
#exec gunicorn -w 1 --threads 4 -k uvicorn.workers.UvicornWorker --proxy-protocol main:app -b :8000
