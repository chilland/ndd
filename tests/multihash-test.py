#!/usr/bin/env python

import sys
import skimage.io as skio

import ndd

orig1 = skio.imread('./data/orig1.jpg')
orig2 = skio.imread('./data/orig2.jpg')
orig3 = skio.imread('./data/orig3.jpg')
dup1  = skio.imread('./data/dup1.jpg')

# --

print '1/2 (Imagehash) Starting'

# Test from scratch
nh = ndd.Multihash([ndd.Hashlib(), ndd.Imagehash()])
nh.add('orig1', orig1)
nh.add('orig3', orig3)

assert(nh.query(orig1).has_match) # Exact match
assert(~nh.query(orig2).has_match) # No match
assert(nh.query(dup1).has_match) # Near-duplicate

nh.save('dbs/multihash-1')

# Test from load
nh = ndd.Multihash([ndd.Hashlib(), ndd.Imagehash()], 'dbs/multihash-1')
assert(nh.query(orig1).has_match) # Exact match
assert(~nh.query(orig2).has_match) # No match
assert(nh.query(dup1).has_match) # Near-duplicate

print "1/2 Success!"

# --

print '2/2 (ConvNet) Starting'

# Test from scratch
nh = ndd.Multihash([ndd.Hashlib(), ndd.ConvNet(model_path='./models/vgg16')])
nh.add('orig1', orig1)
nh.add('orig3', orig3)

assert(nh.query(orig1).has_match) # Exact match
assert(~nh.query(orig2).has_match) # No match
assert(nh.query(dup1).has_match) # Near-duplicate

nh.save('dbs/multihash-2')

# Test from load
nh = ndd.Multihash([ndd.Hashlib(), ndd.ConvNet()], 'dbs/multihash-2')
assert(nh.query(orig1).has_match) # Exact match
assert(~nh.query(orig2).has_match) # No match
assert(nh.query(dup1).has_match) # Near-duplicate

print "2/2 Success!"

# --

print 'Saving all three'
nh = ndd.Multihash([ndd.Hashlib(), ndd.Imagehash(), ndd.ConvNet(model_path='./models/vgg16')])
nh.add('orig1', orig1)
nh.add('orig3', orig3)
nh.save('dbs/multihash-3')

# -- 

print 'Success !'