#!/bin/bash
source env/bin/activate
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app -b :9000 --reload
