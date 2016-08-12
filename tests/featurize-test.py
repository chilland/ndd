#!/usr/bin/env python

'''
    featurize-test.py
    
    Test featurizing a directory of images
    
'''

import sys
import ndd
import h5py
import argparse
import numpy as np
from glob import glob

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inpath', type=str, default='./data/*jpg')
    parser.add_argument('--outpath', type=str, default='./db.h5')
    parser.add_argument('--verbose', action="store_true")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    print >> sys.stderr, 'featurizing %s -> %s' % (args.inpath, args.outpath) 
    
    nh = ndd.Multihash([ndd.Hashlib(), ndd.Imagehash(), ndd.ConvNet()])
    db = h5py.File(args.outpath)

    for file in glob(args.inpath):
        if verbose:
            print >> sys.stderr, file
        
        img = ndd.utils.load_img(file)
        hashes = nh.hash_function(img)
        for method,hash_ in zip(nh.methods, hashes):
            dataset_name = '%s/%s' % (file, method)
            if dataset_name not in db:
                _ = db.create_dataset(dataset_name, data=hash_)
            else:
                print >> sys.stderr, '!! %s \t already exists' % dataset_name

    db.close()
