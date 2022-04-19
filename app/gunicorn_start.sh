#!/bin/bash
#source env/bin/activate
export PATH=$HOME/.local/bin:$PATH
exec gunicorn -w 1 --threads 12 -k uvicorn.workers.UvicornWorker --proxy-protocol main:app -b :8000
