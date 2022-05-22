#!/usr/bin/env python3
import random
from cv2 import cv2
import numpy as np
from time import sleep
import argparse
import os


#Classificatio library
from keras.models import load_model
#from keras.preprocessing.image import load_img
#from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import decode_predictions
from keras.applications.vgg16 import VGG16
from keras.models import load_model
from collections import deque


import cv2
import numpy as np

# CARREGA AS CLASSES
class_names = []
with open("coco.names", "r") as f:
    class_names = [cname.strip() for cname in f.readlines()]

# CAPTURA DO VIDEO
cap = cv2.VideoCapture("unifap.MOV")

# CARREGANDO OS PESOS DA REDE NEURAL
net = cv2.dnn.readNet("yolov4.weights", "yolov4.cfg ")

# SETANDO OS PARAMETROS DA REDE NEURAL
model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(416, 416), scale=1/255)


def detection(frame):
    # DETECÇÃO
    classes, scores, boxes = model.detect(frame, 0.1, 0.2)

    # PERCORRER TODAS AS DETECCÕES
    for (classid, score, box) in zip(classes, scores, boxes):

        # PEGANDO O NOME DA CLASSE PELO ID E O SEU SCORE DE ACURACIA
        label = f"{class_names[classid]}"

        if label == "car" or label == "truck":
            # DE SENHANDO A BOX DA DETECCAO
            redColor = (0, 128, 0)
            cv2.rectangle(frame, box, redColor, 2)

            # ESCREVENDO O NOME DA CLASSE EM CIMA DA BOX DO OBJETO
            cv2.putText(frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, redColor, 2)

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

    newFrame = detection(frame);

    #MOSTRANDO A IMAGEM
    cv2.imshow("detections", newFrame)

    #ESPERA DA RESPOSTA
    if cv2.waitKey(1) == 27:
        break

# LIBERAÇÃO DA CAMERA E DESTROI TODAS AS JANELAS
cap.release()
cv2.destroyAllwindows()












model = load_model("Cinto.model")
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'

# (450, 900, 650, 1000)
# (850, 300, 1350, 800)
parser = argparse.ArgumentParser()
parser.add_argument('-v', '--video_source', dest='video_source',
                    help="Arquivo de origem do vídeo ou índice da câmera alvo", default="video.mp4")
parser.add_argument('-r', '--region_of_interest', dest='roi',
                    help="Região de interesse (start_x, start_y, end_x, end_y,)", default=(300, 300, 1600, 1000))
parser.add_argument('-cfg', '--model_cfg', dest='cfg', help="Arquivo de configuração da rede YOLOv3",
                    default="yolov3.cfg")
parser.add_argument('-w', '--model_weights', dest='weights', help="Arquivo de pesos da rede YOLOv3",
                    default="yolov3.weights")
parser.add_argument('-s', '--scale', dest='scale', help="Escala da rede", default=320)
parser.add_argument('-ct', '--confidence_threshold', dest='ct', help="Tolerância de confiabilidade das detecções",
                    default=0.005)
parser.add_argument('-nms', '--nms_threshold', dest='nms', help="Tolerância de caixas limitantes sobrepostas",
                    default=0.04)
args = parser.parse_args()


# Altere essas variáveis para definir área de interesse
start_x, start_y, end_x, end_y = (args.roi[i] for i in range(4))

scale = 320

# Altere esse variável para alterar a tolerância de confiabilidade do resultado
# Define o quão confiável um resultado deve ser para não ser descartado
confidence_threshold = args.ct

# Altere esse variável para alterar a tolerância de caixas limitantes sobrepostas
# Quanto menor, menos caixas (reduza se encontrar muitas caixas sobrepostas, aumente caso esteja ignorando muitas detecções)
nms_threshold = args.nms

global cars_counter
cars_counter = 0
global bikes_counter
bikes_counter = 0
global persons_counter
persons_counter = 0

global already_counted
already_counted = False

cap = cv2.VideoCapture("unifap2.MOV")

classes_file = 'coco.names'
class_names = []


def find_objects2(outputs, img, object_name, object_name2, save, carro):
    # Lê o formato da imagem
    height, width = img.shape[0], img.shape[1]

    # Define listas de caixa limitante, identificadores de classes e valores de confiabilidade de cada objeto detectado
    bounding_boxes = []
    class_ids = []
    confidence_values = []

    # Para cada uma das saídas
    for output in outputs:
        # Para cada detecção da saída
        for detection in output:
            # Retira os 5 primeiros valores (que indicam as propriedades da detecção)
            scores = detection[5:]
            # Verifica a classe mais provável
            class_id = np.argmax(scores)
            # Verifica a confiabilidade do resultado
            confidence = scores[class_id]

            # Se a confiabilidade for maior do que a tolerância, adiciona a detecção na lista, como uma detecção válida
            if confidence > confidence_threshold:
                # Lê a largura e altura
                w, h = int(detection[2] * width), int(detection[3] * height)
                # Lê o centro da detecção (manipulando os dados da caixa limitante)
                x, y = int((detection[0] * width) - (w / 2)
                           ), int((detection[1] * height) - (h / 2))
                # Adiciona nas listas
                bounding_boxes.append([x, y, w, h])

                class_ids.append(class_id)
                confidence_values.append(float(confidence))

    # Aplica um filtro para caixas limitantes sobrepostas, mantendo apenas a mais confiável
    indices = cv2.dnn.NMSBoxes(
        bounding_boxes, confidence_values, confidence_threshold, nms_threshold)

    if len(indices) == 0:
        globals()['already_counted'] = False

    for i in indices:
        i = i - 1
        box = bounding_boxes[i]
        x, y, w, h = (box[i] for i in range(4))

        if class_names[class_ids[i]] == object_name or class_names[class_ids[i]] == object_name2:
            chopped_object = img[y:y + h, x:x + w]

            if len(chopped_object) > 0:
                if save:
                    x1, x2, y1, y2, wc = carro
                    if x >= x1 and (x+w) <= x2 and y >= y1 and (y+h) <= y2:
                        #print("Altura: " + str(x2) + ", Largura: " + str(y2))


                        chopped_object_resized = cv2.resize(chopped_object, (128, 128))
                        score0 = classification(chopped_object_resized)

                        #if score0 * 100 > 50:
                            #print(" %.2f sem cinto " % (100 * score0))
                        #else:
                            #print(" %.2f com cinto " % (100 * score0))


                        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

                        if score0*100 <50:
                            if x+(w/2) < x1+wc/2:
                                print("Posição carro: "+str(x1+wc/2)+"; Posição pessoa: "+str(x)+". R: Passageiro com Cinto ")
                                cv2.putText(img, "Passageiro Com Cinto", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (36, 255, 12),
                                            2)

                                cv2.imwrite("Pessoas/PCCh" + str(y) + "r" + str(random.randint(0, 100)) + '.png',
                                            chopped_object_resized)
                            else:
                                print("Posição carro: " + str(x1+wc/2) + "; Posição pessoa: " + str(x)+". R: Motorista com Cinto ")
                                cv2.putText(img, "Motorista Com Cinto", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.2,
                                            (36, 255, 12),
                                            2)

                                cv2.imwrite("Pessoas/MCCh" + str(y) + "r" + str(random.randint(0, 100)) + '.png',
                                            chopped_object_resized)

                        else:
                            if x+(w/2) < x1+wc/2:
                                print("Posição carro: " + str(x1+wc/2) + "; Posição pessoa: " + str(x)+". R: Passageiro Sem Cinto ")
                                cv2.putText(img, "Passageiro Sem Cinto ", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (36, 255, 12), 2)
                                cv2.imwrite("Pessoas/PSCh" + str(y) + "r" + str(random.randint(0, 100)) + '.png',
                                            chopped_object_resized)
                            else:
                                print("Posição carro: " + str(x1+wc/2) + "; Posição pessoa: " + str(x)+". R: Motorista Sem Cinto ")
                                cv2.putText(img, "Motorista Sem Cinto ", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.2,
                                            (36, 255, 12), 2)
                                cv2.imwrite("Pessoas/MSCh" + str(y) + "r" + str(random.randint(0, 100)) + '.png',
                                            chopped_object_resized)



                    else:
                        print('-----------------------')
                        print('pessoa fora do carro: ')
                        print(str(x)+'<='+ str(x1)+' ou ' + str(x+w)+'>='+ str(x2))
                        print('ou')
                        print(str(y)+'<='+ str(y1)+' ou ' + str(y+h)+'>='+ str(y2))
                        print('-----------------------')
                else:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    corte = x, x + w, y, y + h, w
                    return corte





def main():
    layer_names = net.getLayerNames()
    out_indices = net.getUnconnectedOutLayers()

    output_names = [layer_names[i - 1] for i in out_indices]
    result = cv2.VideoWriter('result.avi', cv2.VideoWriter_fourcc(*'XVID'), 30.0, (1280, 720))

    while True:
        # Lê a imagem
        success, img = cap.read()
        tempo = float(1 / 50)
        sleep(tempo)

        if success:
            tempo = float(1 / 999)
            sleep(tempo)
            # Recorta a área de interesse
            cropped = img[start_y:end_y, start_x:end_x]
            #cropped = img
            # Desenha um retângulo na área de interesse
            cv2.rectangle(img, (start_x, start_y),
                          (end_x, end_y), (255, 255, 255), 2)

            # Cria um Blob a partir da imagem
            blob = cv2.dnn.blobFromImage(
                cropped, 1 / 255, (scale, scale),
                [0, 0, 0], 1,
                crop=False
            )

            # Define o Blob como a entrada da Rede
            net.setInput(blob)

            # Lê as camadas de saída
            outputs = net.forward(output_names)

            # Encontra os objetos na imagem
            carrotroll = 0,0,0,0
            carro = find_objects2(outputs, cropped, 'car', 'truck', False, carrotroll)
            imgPessoa = outputs
            if carro is not None:
                imgPessoa = find_objects2(outputs, cropped, 'person', 'dasdsa', True, carro)

            # find_objects2(outputs, cropped, 'person', True)

            # Mostra a imagem computada
            cv2.imshow('Contador', img)

            result.write(img)

        if cv2.waitKey(1) == 27:
            break

    result.release()
    cap.release()
    cv2.destroyAllWindows()

    print(cars_counter, " ", bikes_counter)


def SimulatorImagem():
    bodyImage = cv2.imread('teste4cc.PNG')
    score0 = classification(bodyImage)
    if score0*100 > 40:
        print(" %.2f sem cinto " % (100 * score0))
    else:
        print(" %.2f com cinto " % (100 * score0))


    bodyImage2 = cv2.imread('teste3sc.PNG')
    score0 = classification(bodyImage2)
    #if score0 * 100 > 40:
      #  print(" %.2f sem cinto " % (100 * score0))
    #else:
     #   print(" %.2f com cinto " % (100 * score0))


#main()
#SimulatorImagem()