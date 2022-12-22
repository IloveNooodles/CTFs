#!/bin/sh

docker-compose build
docker-compose up -d

if [ "$1" ]; then
  # Put flag in / directory
  filename="/flag-`cat /dev/urandom | base64 | head -c 32 |  tr -d '/+'`.txt"
  docker-compose exec node sh -c "echo $1 > $filename"
fi
