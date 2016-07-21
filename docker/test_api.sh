#!/bin/bash

echo "trying image in index"
curl -XPOST -H "Content-Type:application/json" http://localhost:5000/api/score -d '{
    "url" : "https://pbs.twimg.com/profile_images/551143684671291392/Nx_lx21L_400x400.jpeg"
}'
