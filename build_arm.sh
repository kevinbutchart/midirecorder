#!/bin/bash
TAG_VERSION="1.0"
docker buildx build --platform linux/arm64 -t kevinbutchart/pianorecorder:latest -t kevinbutchart/pianorecorder:"$TAG_VERSION" --push app
