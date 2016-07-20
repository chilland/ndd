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

assert(len(nh.query(orig1)) == 1) # Exact match
assert(len(nh.query(orig2)) == 0) # No match
assert(len(nh.query(dup1)) == 1) # Near-duplicate

nh.save('dbs/multihash')

# Test from load
nh = ndd.Multihash([ndd.Hashlib(), ndd.Imagehash()], 'dbs/multihash')
assert(len(nh.query(orig1)) == 1) # Exact match
assert(len(nh.query(orig2)) == 0) # No match
assert(len(nh.query(dup1)) == 1) # Near-duplicate