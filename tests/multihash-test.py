#!/usr/bin/env python

'''
    multihash-test.py
    
    Test Multihash class
'''


import sys
import ndd

orig1 = ndd.utils.load_img('./data/orig1.jpg')
orig2 = ndd.utils.load_img('./data/orig2.jpg')
orig3 = ndd.utils.load_img('./data/orig3.jpg')
dup1  = ndd.utils.load_img('./data/dup1.jpg')

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
nh = ndd.Multihash([ndd.Hashlib(), ndd.ConvNet()])
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
nh = ndd.Multihash([ndd.Hashlib(), ndd.Imagehash(), ndd.ConvNet()])
nh.add('orig1', orig1)
nh.add('orig3', orig3)
nh.save('dbs/multihash-3')

# -- 

print 'Success !'