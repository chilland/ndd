import sys
import cv2

import ndd

orig1 = cv2.imread('./data/orig1.jpg')
orig2 = cv2.imread('./data/orig2.jpg')
orig3 = cv2.imread('./data/orig3.jpg')
dup1  = cv2.imread('./data/dup1.jpg')

# Test from scratch
nh = ndd.Multihash([ndd.Hashlib(), ndd.Imagehash()])
nh.add('orig1', orig1)
nh.add('orig3', orig3)

assert(nh.query(orig1).has_match) # Exact match
assert(~nh.query(orig2).has_match) # No match
assert(nh.query(dup1).has_match) # Near-duplicate

nh.save('dbs/multihash')

# Test from load
nh = ndd.Multihash([ndd.Hashlib(), ndd.Imagehash()], 'dbs/multihash')
assert(nh.query(orig1).has_match) # Exact match
assert(~nh.query(orig2).has_match) # No match
assert(nh.query(dup1).has_match) # Near-duplicate