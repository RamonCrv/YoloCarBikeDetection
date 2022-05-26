import tensorflow as tf
import numpy as np
from collections import deque
from keras.models import load_model

import cv2
import cvlib

class BeltDetection():


    def __init__(self):
        self.model = load_model('models/belts.model')

    def detectUnbeltedDriver(self, img):
        unbelted = self.detectUnbeltedPerson(img)       
        
        return unbelted


    def detectUnbeltedPassenger(self, img):
        unbelted = self.detectUnbeltedPerson(img)        
        
        return unbelted

    def detectUnbeltedPerson(self, img):
        frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (128, 128)).astype("float32")
        frame = np.expand_dims(frame, 0)  # Create batch axis
        preds = self.model.predict(frame)
        score = preds[0]

        if score*100 > 40:
            return True
        else:
            return False

