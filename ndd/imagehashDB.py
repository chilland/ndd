"""
    imagehash.py
    
    Perceptual hashing via `imagehash` library
"""

import os
import sys
import imagehash
import numpy as np
from PIL import Image

class imagehash:
    ids = np.array([])
    hashes = None
    
    def __init__(self, db_path=None, mode='phash'):
        self.hash_function = lambda x: np.hstack(getattr(imagehash, mode)(Image.open(x)).hash)
        if db_path:
            self.ids, self.hashes = self.load(db_path)
    
    def _hamming(self, x, y):
        return (x != y).sum(axis=1)
        
    def _neighbors(self, x, y, threshold=0):
        return np.where(self._hamming(x, y) <= threshold)[0]
    
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
        
    def query(self, data):
        hsh = self.hash_function(data)
        return self.ids[self._neighbors(hsh, self.hashes)]
    
    def load(self, db_path):
        ids = np.load(os.path.join(db_path, 'ids.npy'))
        hashes = np.load(os.path.join(db_path, 'hashes.npy'))
        return ids, hashes
    
    def save(self, db_path):
        if not os.path.exists(db_path):
            os.makedirs(db_path)
        
        np.save(os.path.join(db_path, 'ids'), self.ids)
        np.save(os.path.join(db_path, 'hashes'), self.hashes)