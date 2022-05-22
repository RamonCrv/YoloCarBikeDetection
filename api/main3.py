
from cv2 import cv2
import cv2
import numpy as np
import random

from scripts.classification_class import Classification
from scripts.car_detection_class import CarDetection
from scripts.belt_detection_class import BeltDetection


video = cv2.VideoCapture("inputs/unifap.MOV")
        
        
classification = Classification()
print(classification.analize(video, 'belt'))


