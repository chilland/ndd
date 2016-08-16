"""
   convnetDB.py
   
   Deep convolutional neural network "hashing" (via `keras` library)
"""

import os
import sys
import numpy as np
from PIL import Image

import ndd
from ndd.convnet_resources import preprocess_input, VGG16

class ConvNet:
    method = 'vgg16_fc7'
    img_size = 224
    
    def __init__(self, db_path=None, verbose=False):
        self.verbose = verbose
                
        if db_path:
            self.load(db_path)
        else:            
            self.ids, self.hashes = np.array([]), None
        
        whole_model = VGG16(include_top=True)
        self.model = Model(input=whole_model.input, output=whole_model.get_layer('fc2').output)
    
    def _dist_function(self, x, y):
        """ Cosine distance """
        return 1 - y.dot(x)
    
    def hash_function(self, img):
        """ CNN featurization """
        if self.verbose:
            print >> sys.stderr, "!! ALWAYS DOUBLE CHECK IMAGE PREPROCESSING"

        img = img.resize((self.img_size, self.img_size), Image.ANTIALIAS)
        img = ndd.utils.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = preprocess_input(img)
        
        pred = self.model.predict(img).squeeze()
        pred /= np.sqrt((pred ** 2).sum())
        return pred
    
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
    
    def query(self, data, threshold=0.05, **kwargs):
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
