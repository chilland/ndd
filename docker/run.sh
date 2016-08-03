#!/bin/bash

docker kill $(docker ps -q) 
docker build -t ndd .
docker run -t -p 5000:5000 ndd
