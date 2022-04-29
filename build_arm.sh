#!/bin/bash
TAG_VERSION="latest"
docker buildx build --platform linux/arm64/v8 -t kevinbutchart/pianorecorder:"$TAG_VERSION" -f app/Dockerfile64 --push app
