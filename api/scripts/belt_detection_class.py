import tensorflow as tf
import numpy as np
from collections import deque
from keras.models import load_model

import cv2
import cvlib

class BeltDetection():


    def __init__(self):
        x = ""
        self.model = load_model('models/belts.model')

    def detectUnbeltedDriver(self, img):
        unbelted = True        
        
        return unbelted


    def detectUnbeltedPassenger(self, img):
        unbelted = True        
        
        return unbelted