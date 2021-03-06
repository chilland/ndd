"""
    imagehashDB.py
    
    Perceptual hashing via `imagehash` library
"""

import os
import sys
import numpy as np
from PIL import Image
import scipy.fftpack

import ndd

class Imagehash(object):
    method = 'phash'
    
    def __init__(self, db_path=None, verbose=False):
        self.verbose = verbose
        if db_path:
            self.load(db_path)
        else:
            self.ids, self.hashes = np.array([]), None
    
    def _dist_function(self, x, y):
        """ Hamming distance """
        return (x != y).sum(axis=1)
    
    def hash_function(self, img, hash_size=8, highfreq_factor=4):
        """ 
            Perceptual hash
            Implementation follows http://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html
            @img must be 2d numpy array representing a greyscale img
            (Taken from `imagehash` library)
        """
        img_size = hash_size * highfreq_factor
        
        img = img.convert("L").resize((img_size, img_size), Image.ANTIALIAS)
        img = np.array(img.getdata(), dtype=np.float).reshape((img_size, img_size))
        
        dct = scipy.fftpack.dct(scipy.fftpack.dct(img, axis=0), axis=1)
        dctlowfreq = dct[:hash_size, :hash_size]
        diff = dctlowfreq > np.median(dctlowfreq)
        return np.hstack(diff)
    
    def add(self, id, data):
        if id not in self.ids:
            hsh = self.hash_function(data)
            self.ids = np.append(self.ids, id)
            if np.any(self.hashes):
                self.hashes = np.vstack((self.hashes, hsh))
            else:
                self.hashes = np.array([hsh])
        else:
            print >> sys.stderr, '!! `id` already exists'
        
    def query(self, data, threshold=0, **kwargs):
        dists = self._dist_function(self.hash_function(data), self.hashes)
        if np.min(dists) <= threshold:
            return ndd.match(**{
                "min_dist" : np.min(dists),
                "matches" : set(self.ids[dists <= threshold]),
                "method" : self.method
            })
        else:
            return ndd.match(method=self.method)
    
    def load(self, db_path):
        self.ids = np.load(os.path.join(db_path, 'ids.npy'))
        self.hashes = np.load(os.path.join(db_path, 'hashes.npy'))
    
    def save(self, db_path):
        if not os.path.exists(db_path):
            os.makedirs(db_path)
        
        np.save(os.path.join(db_path, 'ids'), self.ids)
        np.save(os.path.join(db_path, 'hashes'), self.hashes)