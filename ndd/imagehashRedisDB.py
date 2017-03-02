"""
    imagehashRedisDB.py
    
    Perceptual hashing via `imagehash` library
    Storage via Redis
"""

import ndd

class ImagehashRedis(ndd.Imagehash):
    
    def __init__(self, redis_service='localhost:6379', default_port=6379, verbose=False, prefix="ndd:imagehash"):
        self.con = ndd.utils.get_redis_connection(redis_service, default_port=default_port)
        self.prefix = prefix
    
    def hash_function(self, img, hash_size=8, highfreq_factor=4):
        hsh = super(ImagehashRedis, self).hash_function(img, hash_size, highfreq_factor)
        return ''.join(map(str, hsh.astype('int')))
    
    def add(self, id, data):
        hsh = self.hash_function(data)
        self.con.sadd('%s:%s' % (self.prefix, hsh), id)
    
    def query(self, data, threshold=0, **kwargs):
        hsh = self.hash_function(data)
        
        matches = self.con.smembers('%s:%s' % (self.prefix, hsh))
        if len(matches) > 0:
            return ndd.match(**{
                "min_dist" : 0,
                "matches" : matches,
                "method" : self.method
            })
        else:
            return ndd.match(method=self.method)
    
    def load(self, db_path):
        pass
    
    def save(self, db_path):
        pass
