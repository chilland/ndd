#!/bin/bash

echo "trying image in index"
curl -XPOST -H "Content-Type:application/json" http://localhost:5000/api/score -d '{
    "url" : "/src/data/pos.jpg"
}'

echo "trying image not in index"
curl -XPOST -H "Content-Type:application/json" http://localhost:5000/api/score -d '{
    "url" : "/src/data/neg.jpg"
}'