from cv2 import cv2
import cv2
import numpy as np
import random




class CarDetection():
  def __init__(self):
        # CARREGA AS CLASSES
    self.class_names = []

    # CAPTURA DO VIDEO
    self.cap = cv2.VideoCapture("inputs/unifap.MOV")

    # CARREGANDO OS PESOS DA REDE NEURAL
    self.net = cv2.dnn.readNet("yolo/yolov4.weights", "yolo/yolov4.cfg ")

    # SETANDO OS PARAMETROS DA REDE NEURAL
    self.model = cv2.dnn_DetectionModel(self.net)
    self.model.setInputParams(size=(416, 416), scale=1/255)



  def detectCar(self,frame):

    with open("coco.names", "r") as f:
      self.class_names = [cname.strip() for cname in f.readlines()]

    classes, scores, boxes = self.model.detect(frame, 0.1, 0.2)

    # PERCORRER TODAS AS DETECCÕES
    for (classid, score, box) in zip(classes, scores, boxes):

        # PEGANDO O NOME DA CLASSE PELO ID E O SEU SCORE DE ACURACIA
        label = f"{self.class_names[classid]}"
        
        if label == "car":
            # salva o tamanho e posição do carro
            x, y, w, h = box

            # CORTA O CARRO
            chopped_car = frame[y:y + h, x:x + w]
            if len(chopped_car) > 0:

                # DE SENHANDO A BOX DA DETECCAO
                redColor = (0, 128, 0)
                cv2.rectangle(frame, box, redColor, 2)

                # SALVANDO O CORTE DO CARRO E
                cv2.imwrite("static/outputs/frames/car_" + str(x) + str(y) + str(random.randint(0, 100)) + '.png', chopped_car)

                # ESCREVENDO O NOME DA CLASSE EM CIMA DA BOX DO OBJETO
                cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, redColor, 2)                
                return True

    #return frame
    return False

  def detectDriver(self, frame):
    return True

  def detectPassenger(self, frame):
    return True
    
