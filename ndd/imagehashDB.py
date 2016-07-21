"""
    imagehash.py
    
    Perceptual hashing via `imagehash` library
"""

import os
import sys
import skimage.transform as sktransform
import numpy as np
import scipy.fftpack

import ndd

def phash(image, hash_size=8, highfreq_factor=4):
    """
        Perceptual Hash computation.
        Implementation follows http://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html
        @image must be 2d numpy array representing a greyscale image
        (Taken from `imagehash` library)
    """
    if len(image.shape) != 2:
        raise Exception('!! image must be two dimensional')
    
    img_size = hash_size * highfreq_factor
    image = sktransform.resize(image, (img_size, img_size))
    
    dct = scipy.fftpack.dct(scipy.fftpack.dct(image, axis=0), axis=1)
    dctlowfreq = dct[:hash_size, :hash_size]
    med = np.median(dctlowfreq)
    diff = dctlowfreq > med
    return diff

class Imagehash:
    method = 'phash'
    
    def __init__(self, db_path=None):
        self.hash_function = lambda x: np.hstack(phash(x))
        if db_path:
            self.load(db_path)
        else:
            self.ids, self.hashes = np.array([]), None
    
    def _hamming(self, x, y):
        return (x != y).sum(axis=1)
        
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
        dists = self._hamming(self.hash_function(data), self.hashes)
        if np.min(dists) <= threshold:
            return ndd.match(**{
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