"""
    Query index from a directory of images
    
    Run like:
        python multihash-dir2query.py --input-dir ../tests/data --db ./dbs/test  
    or
        python multihash-dir2query.py --input-dir /Users/bjohnson/projects/sm-image/data/justpasteit/ --db ./db/test
    or
        python multihash-dir2query.py --input-dir ./tmp --db ./dbs/test
"""

import os
import sys
import cv2
import argparse
from glob import glob
import numpy as np

import ndd

def parse_args():
    parser = argparse.ArgumentParser(usage="create hash databases from a directory")
    parser.add_argument('--input-dir', type=str, required=True)
    parser.add_argument('--db', type=str, required=True)
    parser.add_argument('--threshold', type=int, required=False, default=0)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    nh = ndd.Multihash([ndd.Hashlib(), ndd.Imagehash()], args.db)
    for f in glob(os.path.join(args.input_dir, '*')):
        if 'jpg' in f:
            img = cv2.imread(f)
            if np.any(img):
                res = nh.query(img, threshold=0)
                print f, res.to_json()
    