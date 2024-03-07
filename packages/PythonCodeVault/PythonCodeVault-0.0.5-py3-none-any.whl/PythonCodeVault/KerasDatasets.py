# https://medium.com/analytics-vidhya/write-your-own-custom-data-generator-for-tensorflow-keras-1252b64e41c3

import numpy as np
from keras.utils import Sequence

import os
import cv2
import random
import json


class BinaryClassificationDataset(Sequence):
    def __init__(self, path = './data', fail_folder = 'Fail', pass_folder = 'Pass', batch_size = 32, augmentations = None, shuffle_data = True, extension = 'tiff', json_shape = (224,224,1), dtype = np.float32):
        self.fail_path = os.path.join(path, fail_folder)
        self.pass_path = os.path.join(path, pass_folder)
        
        self.extension = extension
        self.dtype = dtype

        self.fail_filepaths = [os.path.join(self.fail_path, filename) for filename in os.listdir(self.fail_path) if filename.endswith(self.extension)]    # Fail == 0
        self.pass_filepaths = [os.path.join(self.pass_path, filename) for filename in os.listdir(self.pass_path) if filename.endswith(self.extension)]    # Pass == 1

        self.json_shape = json_shape

        self.read_images()

        self.fail_tuples = [(img, 1) for img in self.fail_images]
        self.pass_tuples = [(img, 0) for img in self.pass_images]

        self.data = self.fail_tuples + self.pass_tuples
        
        self.shuffle = shuffle_data
        self.batch_size = batch_size
        self.augmentations = augmentations


    def __len__(self):
        return len(self.data) // self.batch_size

    def shuffle_data(self):
        if self.shuffle:
            random.shuffle(self.data)        

    def __getitem__(self, idx):
        data_tuples = self.data[idx * self.batch_size:(idx + 1) * self.batch_size]

        batch_x = [i[0] for i in data_tuples]
        batch_y = [i[1] for i in data_tuples]

        if self.augmentations: 
            return np.array([self.augmentations(image=x.astype(self.dtype))["image"] for x in batch_x]), np.array(batch_y).astype(self.dtype)
        else: 
            return np.array(batch_x).astype(self.dtype), np.array(batch_y).astype(self.dtype)
    
    def read_images(self):
        if self.extension in ['json', '.json']:
            if not self.json_shape: raise Exception('Give wanted img shape (Height, Width (, Channels))')

            self.fail_images, self.pass_images = [], []

            # Pass Images:
            for path in self.pass_filepaths:
                with open(path, 'r') as f:
                    data = json.load(f)
                img = np.array(data).reshape(self.json_shape)
                self.pass_images.append(img)
            
            # Fail Images:
            for path in self.fail_filepaths:
                with open(path, 'r') as f:
                    data = json.load(f)
                img = np.array(data).reshape(self.json_shape)
                self.fail_images.append(img)
        else:
            self.fail_images = [cv2.imread(path, 0) for path in self.fail_filepaths]
            self.pass_images = [cv2.imread(path, 0) for path in self.pass_filepaths]