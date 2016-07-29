import os
import sys
import ndd
import skimage.io as skio

class apiModel():
    model_name = '%s-ndd-0.0.0'
    
    def __init__(self, db_path):
        self.nh = ndd.Multihash([
            ndd.Hashlib(), 
            ndd.Imagehash(),
            # ndd.ConvNet()
        ], db_path)
    
    def _get_image(self, url):
        return skio.imread(url)
        
    def predict_api(self, **kwargs):
        res = self.nh.query(self._get_image(kwargs['url']))
        return {
            'label': res.has_match,
            'score': res.has_match, # !! Return distance for non-exact queries
            'model': self.model_name % res.method
        }