import os
import ndd

class Multihash:
    """ Wraps multiple `ndd` hashes, checks them in order of complexity """
    def __init__(self, hashes, db_path=None):
        self.hashes = hashes
        if db_path:
            self.load(db_path)
    
    def add(self, id, data):
        for hash_ in self.hashes:
            hash_.add(id, data)
    
    def query(self, data):
        for hash_ in self.hashes:
            curr = hash_.query(data)
            if curr:
                return curr
        
        return set([])
    
    def load(self, db_path):
        subdirs = sorted(os.listdir(db_path))
        for i, hash_ in enumerate(self.hashes):
            hash_.load(os.path.join(db_path, subdirs[i]))
        
    def save(self, db_path):
        for i, hash_ in enumerate(self.hashes):
            hash_.save(os.path.join(db_path, str(i)))