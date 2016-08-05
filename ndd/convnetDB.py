"""
   convnetDB.py
   
   Deep convolutional neural network "hashing" (via `keras` library)
"""

import os
import sys
import numpy as np
from PIL import Image
from keras.models import model_from_json

import ndd
from ndd.convnet_resources import preprocess_input, VGG16

class ConvNet:
    method = 'vgg16_fc7'
    structure_name = 'Keras_model_structure.json'
    weights_name = 'Keras_model_weights.h5'
    img_size = 224
    
    def __init__(self, db_path=None, model_path=None, verbose=False):
        self.verbose = verbose
                
        if db_path:
            self.load(db_path)
        else:            
            self.ids, self.hashes, self.model = np.array([]), None, None
        
        self.model = VGG16()
    
    def _dist_function(self, x, y):
        """ Cosine distance """
        return 1 - y.dot(x)
    
    def _hash_function(self, img):
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
            hsh = self._hash_function(data)
            self.ids = np.append(self.ids, id)
            if np.any(self.hashes):
                self.hashes = np.vstack((self.hashes, hsh))
            else:
                self.hashes = np.array([hsh])
        else:
            print >> sys.stderr, '!! `id` already exists'
    
    def query(self, data, threshold=0.03, **kwargs):
        dists = self._dist_function(self._hash_function(data), self.hashes)
        if np.min(dists) <= threshold:
            return ndd.match(**{
                "min_dist" : np.min(dists),
                "matches" : set(self.ids[dists <= threshold]),
                "method" : self.method
            })
        else:
            return ndd.match(method=self.method)
    
    def _load_model(self, dirpath):
        """
            @dirpath needs to point to directory containing Keras model, 
                w/ JSON and H5 data named as in `structure_name` and `weights_name`
        """
        model = model_from_json(open(os.path.join(dirpath, self.structure_name)).read())
        model.load_weights(os.path.join(dirpath, self.weights_name))
        return model
    
    def load(self, db_path):
        self.ids = np.load(os.path.join(db_path, 'ids.npy'))
        self.hashes = np.load(os.path.join(db_path, 'hashes.npy'))
        
        # Also try to load model
        try:
            self.model = self._load_model(db_path)
        except:
            pass
    
    def _save_model(self, dirpath):
        open(os.path.join(dirpath, self.structure_name), 'w').write(self.model.to_json())
        self.model.save_weights(os.path.join(dirpath, self.weights_name), overwrite=True)
    
    def save(self, db_path):
        if not os.path.exists(db_path):
            os.makedirs(db_path)
        
        np.save(os.path.join(db_path, 'ids'), self.ids)
        np.save(os.path.join(db_path, 'hashes'), self.hashes)
        
        # Also save model in new location
        self._save_model(db_path)
