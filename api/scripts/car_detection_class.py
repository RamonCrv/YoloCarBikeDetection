from cv2 import cv2
import cv2
import numpy as np
import random
from keras.models import load_model



class CarDetection():
  def __init__(self):
        # CARREGA AS CLASSES
    self.class_names = []

    # CAPTURA DO VIDEO
    #self.cap = cv2.VideoCapture("inputs/unifap.MOV")

    # CARREGANDO OS PESOS DA REDE NEURAL
    self.net = cv2.dnn.readNet("yolo/yolov4.weights", "yolo/yolov4.cfg")

    # SETANDO OS PARAMETROS DA REDE NEURAL
    self.model = cv2.dnn_DetectionModel(self.net)
    self.model.setInputParams(size=(416, 416), scale=1/255)


  def detectObjects(self, frame, objectName):

    with open("coco.names", "r") as f:
      self.class_names = [cname.strip() for cname in f.readlines()]

    classes, scores, boxes = self.model.detect(frame, 0.0000001, 0.8) #0.05, 0.04 default

    objectsDetected = []
    # PERCORRER TODAS AS DETECCÕES
    for (classid, score, box) in zip(classes, scores, boxes):

        # PEGANDO O NOME DA CLASSE PELO ID E O SEU SCORE DE ACURACIA
        label = f"{self.class_names[classid]}"
        
        if label == objectName :
            # salva o tamanho e posição do carro
            #x, y, w, h = box
            objectsDetected.append(box)
            # CORTA O CARRO

    return objectsDetected          

  def detectCar(self, frame):
    cars = self.detectObjects(frame, "car")
    return cars    

  def detectDriver(self, frame, car, seconds):    
    persons = self.detectObjects(frame, "person") 
    cx, cy, cw, ch = car
    driver = None
    # PERCORRER TODAS AS DETECCÕES
    for person in persons:
      x, y, w, h = person
      if x >= cx and (x+w) <= (cx+cw) and y >= cy and (y+h) <= (cy+ch): 
        if x+(w/2) > cx+(cw/2):
          driver = frame[y:y + h, x:x + w]
          cv2.imwrite("static/outputs/Persons/driver_" + str(x) + str(y) + "_" + str(seconds) + '.png', driver)
          return True, driver
    return False, driver

  def detectPassenger(self, frame, car, seconds):
    persons = self.detectObjects(frame, "person") 
    cx, cy, cw, ch = car
    passenger = None
    # PERCORRER TODAS AS DETECCÕES
    for person in persons:
      x, y, w, h = person
      if x >= cx and (x+w) <= (cx+cw) and y >= cy and (y+h) <= (cy+ch): 
        if x+(w/2) < cx+(cw/2):
          passenger = frame[y:y + h, x:x + w]
          cv2.imwrite("static/outputs/Persons/passenger_" + str(x) + str(y) + "_" + str(seconds) + '.png', passenger)
          return True, passenger
    return False, passenger
    
