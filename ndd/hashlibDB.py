"""
    hashlib.py

    Exact hashing via `hashlib.md5`
"""

import os
import sys
import pickle
from hashlib import md5

class Hashlib:
    def __init__(self, db_path=None):
        self.hash_function = lambda x: md5(x).hexdigest()
        if db_path:
            self.load(db_path)
        else:
            self.ids, self.hashes = set([]), {}
    
    def add(self, id, data):
        if id not in self.ids:
            hsh = self.hash_function(data)
            
            curr = self.hashes.get(hsh, set([]))
            curr.add(id)
            self.hashes[hsh] = curr
            self.ids.add(id)
        else:
            print >> sys.stderr, '!! `id` already exists'
                
    def query(self, data, **kwargs):
        hsh = self.hash_function(data)
        matches = self.hashes.get(hsh, None)
        if matches:
            return matches, True
        else:
            return set([]), False
    
    def load(self, db_path):
        self.ids = pickle.load(open(os.path.join(db_path, 'ids'), 'r'))
        self.hashes = pickle.load(open(os.path.join(db_path, 'hashes'), 'r'))
        
    def save(self, db_path):
        if not os.path.exists(db_path):
            os.makedirs(db_path)
            
        pickle.dump(self.ids, open(os.path.join(db_path, 'ids'), 'w'))
        pickle.dump(self.hashes, open(os.path.join(db_path, 'hashes'), 'w'))

