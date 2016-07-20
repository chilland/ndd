"""
    Create indices from a directory of images
    
    Run like:
        python multihash-directory.py --input-dir ../tests/data --output-dir ./tmp
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
    parser.add_argument('--output-dir', type=str, required=True)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    nh = ndd.Multihash([ndd.Hashlib(), ndd.Imagehash()])
    counter = 0
    for f in glob(os.path.join(args.input_dir, '*')):
        if 'jpg' in f:
            img = cv2.imread(f)
            if np.any(img):
                nh.add(f, img)
                
                sys.stderr.write("\r\t%d\t%s " % (counter, f))
                sys.stderr.flush()
                counter += 1
                
    print >> sys.stderr, '\n Added %d images' % counter
    nh.save(args.output_dir)