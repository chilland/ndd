#!/usr/bin/env python

import sys
import skimage.io as skio

import ndd

orig1 = skio.imread('./data/orig1.jpg')
orig2 = skio.imread('./data/orig2.jpg')
orig3 = skio.imread('./data/orig3.jpg')
dup1  = skio.imread('./data/dup1.jpg')

# Test from scratch
nh = ndd.ConvNet(model_path='./models/vgg16/')
nh.add('orig1', orig1)
nh.add('orig3', orig3)

assert(nh.query(orig1).has_match) # Exact match
assert(~nh.query(orig2).has_match) # No match
assert(nh.query(dup1).has_match) # Near-duplicate

nh.save('dbs/convnet')

# Test from load
nh = ndd.ConvNet(model_path='./models/vgg16/', db_path='dbs/convnet')
assert(nh.query(orig1).has_match) # Exact match
assert(~nh.query(orig2).has_match) # No match
assert(nh.query(dup1).has_match) # Near-duplicate

print "Success!"