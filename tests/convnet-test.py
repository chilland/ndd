#!/usr/bin/env python

import os
import sys
import skimage.io as skio

import ndd

orig1 = skio.imread('./data/orig1.jpg')
orig2 = skio.imread('./data/orig2.jpg')
orig3 = skio.imread('./data/orig3.jpg')
dup1  = skio.imread('./data/dup1.jpg')

# Check that model files exist
model_path = './models/vgg16'
if not os.path.exists(os.path.join(model_path, 'Keras_model_weights.h5')):
    raise Exception((
        '\n\n\t Keras_model_weights.h5 does not exist! \n'
        '\t Download them at `https://drive.google.com/file/d/0Bz7KyqmuGsilT0J5dmRCM0ROVHc/view\?usp\=sharing`'
    ))

# Test from scratch
nh = ndd.ConvNet(model_path=model_path)
nh.add('orig1', orig1)
nh.add('orig3', orig3)

assert(nh.query(orig1).has_match) # Exact match
assert(~nh.query(orig2).has_match) # No match
assert(nh.query(dup1).has_match) # Near-duplicate

nh.save('dbs/convnet')

# Test from load
nh = ndd.ConvNet(model_path=model_path, db_path='dbs/convnet')
assert(nh.query(orig1).has_match) # Exact match
assert(~nh.query(orig2).has_match) # No match
assert(nh.query(dup1).has_match) # Near-duplicate

print "Success!"
