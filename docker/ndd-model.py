import os
import sys
import ndd

class apiModel():
    def __init__(self, db_path, model_name):
        self.model_name = model_name
        self.nh = ndd.Multihash([
            ndd.Hashlib(), 
            ndd.Imagehash(),
            # ndd.ConvNet() # !! No GPU support yet
        ], db_path)
    
    def predict_api(self, **kwargs):
        res = self.nh.query(ndd.utils.load_img(kwargs['url']))
        return {
            'label': res.has_match,
            'score': res.min_dist,
            'model': '%s-%s' % (self.model_name, res.method)
        }
