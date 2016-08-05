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

