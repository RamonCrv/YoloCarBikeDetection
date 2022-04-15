#!/usr/bin/env python3
import random

from cv2 import cv2
import numpy as np
from time import sleep
import argparse

# (450, 900, 650, 1000)
parser = argparse.ArgumentParser()
parser.add_argument('-v', '--video_source', dest='video_source',
                    help="Arquivo de origem do vídeo ou índice da câmera alvo", default="video.mp4")
parser.add_argument('-r', '--region_of_interest', dest='roi',
                    help="Região de interesse (start_x, start_y, end_x, end_y,)", default=(150, 300, 1500, 800))
parser.add_argument('-cfg', '--model_cfg', dest='cfg', help="Arquivo de configuração da rede YOLOv3",
                    default="yolov3.cfg")
parser.add_argument('-w', '--model_weights', dest='weights', help="Arquivo de pesos da rede YOLOv3",
                    default="yolov3.weights")
parser.add_argument('-s', '--scale', dest='scale', help="Escala da rede", default=320)
parser.add_argument('-ct', '--confidence_threshold', dest='ct', help="Tolerância de confiabilidade das detecções",
                    default=.05)
parser.add_argument('-nms', '--nms_threshold', dest='nms', help="Tolerância de caixas limitantes sobrepostas",
                    default=0.75)
args = parser.parse_args()

# Altere essa variável para utilizar outros videos ou câmeras
video_source = args.video_source

# Altere essas variáveis para definir área de interesse
start_x, start_y, end_x, end_y = (args.roi[i] for i in range(4))

# Altere essas variáveis para utilizar outros modelos pré-treinados do YOLO
model_cfg = "yolov3.cfg"
model_weights = "yolov2.weights"
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

cap = cv2.VideoCapture("334.mp4")

classes_file = 'coco.names'
class_names = []
with open(classes_file, 'rt') as f:
    class_names = f.read().rstrip('\n').split('\n')

net = cv2.dnn.readNet("yolov3-spp.weights", "yolov3-spp.cfg ")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)


def find_objects2(outputs, img, object_name, save, carro):
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
        if class_names[class_ids[i]] == object_name:
            chopped_object = img[y:y + h, x:x + w]

            if len(chopped_object) > 0:
                if save:
                    x1, x2, y1, y2 = carro
                    if x >= x1 and (x+w) <= x2 and y >= y1 and (y+h) <= y2:
                        cv2.imwrite("Pessoas/h" + str(y) + "r" + str(random.randint(0, 100)) + '.jpg', chopped_object)
                        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        cv2.putText(img, "Com Cinto", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (36, 255, 12), 2)
                    else:
                        print('-----------------------')
                        print('pessoa fora do carro: ')
                        print(str(x)+'<='+ str(x1)+' ou ' + str(x+w)+'>='+ str(x2))
                        print('ou')
                        print(str(y)+'<='+ str(y1)+' ou ' + str(y+h)+'>='+ str(y2))
                        print('-----------------------')
                else:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    corte = x, x + w, y, y + h
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
            carro = find_objects2(outputs, cropped, 'car', False, carrotroll)
            if carro is not None:
                find_objects2(outputs, cropped, 'person', True, carro)

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


main()
