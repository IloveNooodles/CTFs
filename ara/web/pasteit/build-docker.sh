#!/bin/bash
docker rm -f web_pasteit
docker build -t web_pasteit . 
docker run --name=web_pasteit --rm -p4512:1339 -it web_pasteit
