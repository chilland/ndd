"""
    utils.py
    
    Utilities for NDD
    
    `load_img` and `img_to_array` are adapted from Keras
"""

import sys
from PIL import Image
import urllib
import cStringIO
import numpy as np
from redis import StrictRedis
from rediscluster import StrictRedisCluster

def load_img(path, grayscale=False, target_size=None):
    if path[:4] == 'http': # Allow loading from http URL
        path = cStringIO.StringIO(urllib.urlopen(path).read())

    img = Image.open(path)
    if grayscale:
        img = img.convert('L')
    else:  # Ensure 3 channel even when loaded image is grayscale
        img = img.convert('RGB')
    if target_size:
        img = img.resize((target_size[1], target_size[0]))
    return img


def img_to_array(img):
    x = np.asarray(img, dtype='float32')
    if len(x.shape) == 3:
        x = x.transpose(2, 0, 1)
    elif len(x.shape) == 2:
        x = x.reshape((1, x.shape[0], x.shape[1]))
    else:
        raise Exception('Unsupported image shape: ', x.shape)
    return x

def get_host_port(connect, default_port=80):
    hostport = connect.split(':')
    if len(hostport) == 2:
        port = int(hostport[1])
    else:
        port = default_port
    
    return hostport[0], port


def get_redis_connection(redis_service, default_port):
    nodes = redis_service.split(',')
    if len(nodes) == 1:
        r_host, r_port = get_host_port(redis_service, default_port=default_port)
        r = StrictRedis(r_host, r_port, db=0)
        print "Single-node Redis connection established."
    else:
        startup_nodes = []
        for node in nodes:
            r_host, r_port = node.split(':')
            startup_nodes.append({'host' : r_host, 'port' : r_port})
        
        r = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)
        print "Multi-node Redis connection established."
    
    return r