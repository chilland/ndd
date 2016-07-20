import sys
import cv2

import ndd

orig1 = cv2.imread('./data/orig1.jpg')
orig2 = cv2.imread('./data/orig2.jpg')
orig3 = cv2.imread('./data/orig3.jpg')
dup1  = cv2.imread('./data/dup1.jpg')

# Test from scratch
nh = ndd.Hashlib()
nh.add('orig1', orig1)
nh.add('orig3', orig3)

assert(nh.query(orig1)[1]) # Exact match
assert(~nh.query(orig2)[1]) # No match
assert(~nh.query(dup1)[1]) # Near-duplicate

nh.save('dbs/hashlib')

# Test from load
nh = ndd.Hashlib('dbs/hashlib')
assert(nh.query(orig1)[1]) # Exact match
assert(~nh.query(orig2)[1]) # No match
assert(~nh.query(dup1)[1]) # Near-duplicate


