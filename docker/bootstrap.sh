#!/bin/bash

apt-get clean && apt-get update
apt-get install -y build-essential g++

mv .keras /root/.keras
pip install -r requirements.txt
