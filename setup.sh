#! /bin/bash

# Instalando dependências
pip3 install -r requirements

# Baixando pesos e configurações da rede
wget https://pjreddie.com/media/files/yolov3.weights
wget https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3.cfg

# Alterando a permissão de execução
sudo chmod +x main.py
