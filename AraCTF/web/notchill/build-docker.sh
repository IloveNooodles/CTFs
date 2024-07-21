#!/bin/bash
docker rm -f web_noctchill_db
docker build -t web_noctchill_db . 
docker run --name=web_noctchill_db --rm -p6712:80 -it web_noctchill_db
