
from cv2 import cv2
import cv2
import numpy as np
import random

# CARREGA AS CLASSES
class_names = []
with open("coco.names", "r") as f:
    class_names = [cname.strip() for cname in f.readlines()]

# CAPTURA DO VIDEO
cap = cv2.VideoCapture("input/unifap.MOV")

# CARREGANDO OS PESOS DA REDE NEURAL
net = cv2.dnn.readNet("yolov4.weights", "yolov4.cfg ")

# SETANDO OS PARAMETROS DA REDE NEURAL
model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(416, 416), scale=1/255)


def car_detection(frame):
    # Lê o formato da imagem
    height, width = frame.shape

    # DETECÇÃO
    classes, scores, boxes = model.detect(frame, 0.1, 0.2)

    # PERCORRER TODAS AS DETECCÕES
    for (classid, score, box) in zip(classes, scores, boxes):

        # PEGANDO O NOME DA CLASSE PELO ID E O SEU SCORE DE ACURACIA
        label = f"{class_names[classid]}"

        # Lê a largura e altura
        w, h = int(box * width), int(box * height)

        # Lê o centro da detecção
        x, y = int((box * width) - (w / 2))

        # CHOP CAR
        chopped_car = frame[y:y + h, x:x + w]

        if label == "car":
            # DE SENHANDO A BOX DA DETECCAO
            redColor = (0, 128, 0)
            cv2.rectangle(frame, box, redColor, 2)

            # ESCREVENDO O NOME DA CLASSE EM CIMA DA BOX DO OBJETO
            cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, redColor, 2)

            # SALVANDO O CORTE DO CARRO E
            cv2.imwrite("output/Pessoas/car" + str(x) + str(y) + str(random.randint(0, 100)) + '.png', chopped_car)


    return frame;

def classification(image):
    frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (128, 128)).astype("float32")
    frame = np.expand_dims(frame, 0)  # Create batch axis
    preds = model.predict(frame)
    score = preds[0]
    return score[0]

while True:
    # CAPTURA DO FRAME
    _, frame = cap.read()

    newFrame = car_detection(frame)

    #MOSTRANDO A IMAGEM
    cv2.imshow("detections", newFrame)

    #ESPERA DA RESPOSTA
    if cv2.waitKey(1) == 27:
        break

# LIBERAÇÃO DA CAMERA E DESTROI TODAS AS JANELAS
cap.release()
cv2.destroyAllwindows()












