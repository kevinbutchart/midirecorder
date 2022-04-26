#!/bin/bash
#source env/bin/activate
export PATH=$HOME/.local/bin:$PATH
exec gunicorn -w 1 --threads 12 -k uvicorn.workers.UvicornWorker --proxy-protocol --certfile=certificate/pianorecorder.pem --keyfile=certificate/pianorecorder.key main:app -b :8443
