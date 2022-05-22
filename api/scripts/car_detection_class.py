from cv2 import cv2
import cv2
import numpy as np
import random




class CarDetection():
  def __init__(self):
    x= ""
    #self.model = tf.keras.models.load_model('models\cnn_activity_gender_dataset_body_50.model')


  def detectCar(frame):

    # CARREGA AS CLASSES
    class_names = []
    with open("coco.names", "r") as f:
        class_names = [cname.strip() for cname in f.readlines()]

    # CAPTURA DO VIDEO
    cap = frame

    # CARREGANDO OS PESOS DA REDE NEURAL
    net = cv2.dnn.readNet("yolo/yolov4.weights", "yolo/yolov4.cfg ")

    # SETANDO OS PARAMETROS DA REDE NEURAL
    model = cv2.dnn_DetectionModel(net)
    model.setInputParams(size=(416, 416), scale=1/255)

    
    return True
