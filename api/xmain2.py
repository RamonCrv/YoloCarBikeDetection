from cv2 import cv2
import cv2
import numpy as np
import random
import sys
from scripts.car_detection_class import CarDetection
from keras.models import load_model

#model = load_model("models/cinto.model")

# CARREGA AS CLASSES
#class_names = []
#with open("coco.names", "r") as f:
#    class_names = [cname.strip() for cname in f.readlines()]

# CAPTURA DO VIDEO
cap = cv2.VideoCapture("static/inputs/unifap_cortado.avi")

# CARREGANDO OS PESOS DA REDE NEURAL
#net = cv2.dnn.readNet("yolo/yolov4.weights", "yolo/yolov4.cfg ")

# SETANDO OS PARAMETROS DA REDE NEURAL
#model = cv2.dnn_DetectionModel(net)
#model.setInputParams(size=(416, 416), scale=1/255)


# def car_detection(frame):
#     # DETECÇÃO
#     classes, scores, boxes = model.detect(frame, 0.1, 0.2)

#     # PERCORRER TODAS AS DETECCÕES
#     for (classid, score, box) in zip(classes, scores, boxes):

#         # PEGANDO O NOME DA CLASSE PELO ID E O SEU SCORE DE ACURACIA
#         label = f"{class_names[classid]}"
        
#         if label == "car":
#             # salva o tamanho e posição do carro
#             x, y, w, h = box

#             # CORTA O CARRO
#             chopped_car = frame[y:y + h, x:x + w]
#             if len(chopped_car) > 0:

#                 # DE SENHANDO A BOX DA DETECCAO
#                 redColor = (0, 128, 0)
#                 cv2.rectangle(frame, box, redColor, 2)

#                 # SALVANDO O CORTE DO CARRO E
#                 cv2.imwrite("outputs/frames/car_" + str(x) + str(y) + str(random.randint(0, 100)) + '.png', chopped_car)

#                 # ESCREVENDO O NOME DA CLASSE EM CIMA DA BOX DO OBJETO
#                 cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, redColor, 2)

#                 #return chopped_car


#     return frame

# def classification(image):
#     frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     frame = cv2.resize(frame, (128, 128)).astype("float32")
#     frame = np.expand_dims(frame, 0)  # Create batch axis
#     preds = model.predict(frame)
#     score = preds[0]
#     return score[0]

while True:
    # CAPTURA DO FRAME
    _, frame = cap.read()
    carDetection = CarDetection()
    newFrame =  carDetection.detectCar(frame)



    #MOSTRANDO A IMAGEM
    cv2.imshow("detections", newFrame)
    #print("new frame")
    #sys.exit()
    #ESPERA DA RESPOSTA
    if cv2.waitKey(1) == 27:
        break

# LIBERAÇÃO DA CAMERA E DESTROI TODAS AS JANELAS
cap.release()
cv2.destroyAllwindows()












