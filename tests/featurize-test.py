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
    
    nh = ndd.Multihash([ndd.Hashlib(), ndd.Imagehash(), ndd.ConvNet()])
    db = h5py.File(args.outpath)

    files = glob(args.inpath)
    print >> sys.stderr, 'featurizing %d images from %s into %s' % (len(files), args.inpath, args.outpath) 
    for file in files:
        if args.verbose:
            print >> sys.stderr, file
        
        # Check if all hashes exist
        dataset_names = ['%s/%s' % (file, method) for method in nh.methods]
        if np.all([dataset_name in db for dataset_name in dataset_names]):
            continue
        
        img = ndd.utils.load_img(file)
        hashes = nh.hash_function(img)
        for dataset_name,hash_ in zip(dataset_names, hashes):
            if dataset_name not in db:
                _ = db.create_dataset(dataset_name, data=hash_)
            else:
                print >> sys.stderr, '!! %s \t already exists' % dataset_name

    db.close()
