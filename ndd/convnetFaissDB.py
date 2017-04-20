"""
   convnetFaissDB.py
   
   Deep convolutional neural network "hashing" (via `keras` library)
   Index features w/ `faiss`
"""

import os
os.environ['KERAS_BACKEND'] = 'theano'
import keras.backend as K
K.set_image_dim_ordering('th')

import sys
import numpy as np
from PIL import Image

from keras.models import Model
from keras.preprocessing import image
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input

import faiss

import ndd

class ConvNetFaiss(object):
    method = 'vgg16_fc7'
    img_size = 224
    feat_size = 4096
    
    def __init__(self, db_path=None, verbose=False):
        self.verbose = verbose
        
        whole_model = VGG16(weights='imagenet', include_top=True)
        self.model = Model(input=whole_model.input, output=whole_model.get_layer('fc2').output)
        
        if db_path:
            self.load(db_path)
        else:
            self.ids, self.hashes = np.array([]), faiss.IndexFlatIP(self.feat_size)
    
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
            self.hashes.add(hsh.reshape(1, -1))
        else:
            print >> sys.stderr, '!! `id` already exists'
            
    def query(self, data, threshold=0.05, **kwargs):
        D, I = self.hashes.search(self.hash_function(data).reshape(1, -1), 1)
        min_dist = 1 - float(D.squeeze())
        if min_dist <= threshold:
            return ndd.match(**{
                "min_dist": min_dist,
                "matches": set([self.ids[int(I.squeeze())]]),
                "method": self.method
            })
        else:
            return ndd.match(method=self.method)
            
    def load(self, db_path):
        self.ids = np.load(os.path.join(db_path, 'ids.npy'))
        self.hashes = faiss.read_index(os.path.join(db_path, 'hashes.faiss'))
        
    def save(self, db_path):
        if not os.path.exists(db_path):
            os.makedirs(db_path)
            
        np.save(os.path.join(db_path, 'ids'), self.ids)
        faiss.write_index(self.hashes, os.path.join(db_path, 'hashes.faiss'))
