import tensorflow as tf
import numpy as np
from collections import deque
from keras.models import load_model

import cv2
import cvlib

class BeltDetection():


    def __init__(self):
        x = ""
        self.model = tf.keras.models.load_model('models/cinto_300_50.model')

    def detectUnbeltedDriver(self, img):
        unbelted = True
        var_size = 128

        faces = self.detect_faces(img)

        if len(faces) == 0:
            faces = self.detect_faces2(img)

        if len(faces) == 0:
            faces = [img]

        for frame in faces:
        # initialize the image mean for mean subtraction along with the predictions queue
            mean = np.array([123.68, 116.779, 103.939][::1], dtype="float32")
            Q = deque(maxlen=var_size)
        
            # clone the output frame, then convert it from BGR to RGB perform mean subtraction
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (224, 224)).astype("float32")
            frame -= mean
            
            # make predictions on the frame and then update the predictions
            frame = np.expand_dims(frame, 0)  # Create batch axis

            preds = self.model.predict(frame)
            score = preds[0]
            
            result = " %.2f man | %.2f woman." % (100 * score[0], 100 * score[1])
            print(result)
            
            if score[1] >= 0.5:
                unbelted = False
        
        return unbelted


    def detectUnbeltedPassenger(self, img):
        unbelted = True
        var_size = 128

        faces = self.detect_faces(img)

        if len(faces) == 0:
            faces = self.detect_faces2(img)

        if len(faces) == 0:
            faces = [img]

        for frame in faces:
        # initialize the image mean for mean subtraction along with the predictions queue
            mean = np.array([123.68, 116.779, 103.939][::1], dtype="float32")
            Q = deque(maxlen=var_size)
        
            # clone the output frame, then convert it from BGR to RGB perform mean subtraction
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (224, 224)).astype("float32")
            frame -= mean
            
            # make predictions on the frame and then update the predictions
            frame = np.expand_dims(frame, 0)  # Create batch axis

            preds = self.model.predict(frame)
            score = preds[0]
            
            result = " %.2f man | %.2f woman." % (100 * score[0], 100 * score[1])
            print(result)
            
            if score[1] >= 0.5:
                unbelted = False
        
        return unbelted