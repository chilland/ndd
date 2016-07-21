import sys
import skimage.io as skio

import ndd

orig1 = skio.imread('./data/orig1.jpg', as_grey=True)
orig2 = skio.imread('./data/orig2.jpg', as_grey=True)
orig3 = skio.imread('./data/orig3.jpg', as_grey=True)
dup1  = skio.imread('./data/dup1.jpg', as_grey=True)

# Test from scratch
nh = ndd.Imagehash()
nh.add('orig1', orig1)
nh.add('orig3', orig3)

assert(nh.query(orig1).has_match) # Exact match
assert(~nh.query(orig2).has_match) # No match
assert(nh.query(dup1).has_match) # Near-duplicate

nh.save('dbs/imagehash')

# Test from load
nh = ndd.Imagehash('dbs/imagehash')
assert(nh.query(orig1).has_match) # Exact match
assert(~nh.query(orig2).has_match) # No match
assert(nh.query(dup1).has_match) # Near-duplicate
