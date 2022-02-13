#!/bin/bash
TAG_VERSION="1.0"
docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7 -t kevinbutchart/pianorecorder:latest -t kevinbutchart/pianorecorder:"$TAG_VERSION" --push app
