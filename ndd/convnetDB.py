"""
   convnetDB.py
   
   Deep convolutional neural network "hashing" (via `keras` library)
"""

import os
import sys
import numpy as np
import skimage.transform as sktransform
from keras.models import model_from_json

import ndd

class ConvNet:
    method = 'vgg16_fc7'
    structure_name = 'Keras_model_structure.json'
    weights_name = 'Keras_model_weights.h5'
    
    def __init__(self, model_path, db_path=None, verbose=False):
        self.model = self._load_model(model_path)
        self.verbose = verbose
        if db_path:
            self.load(db_path)
        else:
            self.ids, self.hashes = np.array([]), None
    
    def _load_model(self, model_path):
        """ 
            
        """
        model = model_from_json(open(os.path.join(model_path, self.structure_name)).read())
        model.load_weights(os.path.join(model_path, self.weights_name))
        return model
    
    def _dist_function(self, x, y):
        """ Cosine distance """
        return 1 - y.dot(x)
    
    def _hash_function(self, img):
        """ CNN featurization """
        if self.verbose:
            print >> sys.stderr, "!! ALWAYS DOUBLE CHECK IMAGE PREPROCESSING"
        
        img = sktransform.resize(img, self.model.input_shape[2:]) # Resize image to fit into network
        img = img.transpose((2, 0, 1)) # Transpose to appropriate shape
        img = img.astype('float32') / 255 # Scale RGB values
        
        return self.model.predict(img[np.newaxis,...]).squeeze()
    
    def add(self, id, data):
        if id not in self.ids:
            hsh = self._hash_function(data)
            self.ids = np.append(self.ids, id)
            if np.any(self.hashes):
                self.hashes = np.vstack((self.hashes, hsh))
            else:
                self.hashes = np.array([hsh])
        else:
            print >> sys.stderr, '!! `id` already exists'
    
    def query(self, data, threshold=0, **kwargs):
        dists = self._dist_function(self._hash_function(data), self.hashes)
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