# Contador de Veículos

Aplicação em Python utilizando YOLO e OpenCV para detecção e contagem de carros e motos em um vídeo.
[Video DEMO](https://youtu.be/jbuc8bR1FSs)

# Instalação e execução

## Clonando o Repositório

    $ git clone https://github.com/GPoleto27/contador_de_veiculos

## Instalando as dependências, configurações e pesos da rede

    $ cd contador_de_veiculos
    $ sudo chmod +x setup.sh
    $ ./setup.sh

## Execute a aplicação

    $ ./main.py

# Customização da aplicação

## Alterando a fonte do vídeo

Adicione o argumento _-v_ ou *--video_source*

> Altere essa variável para utilizar outros videos ou câmeras.

Você pode usar seu próprio arquivo de vídeo ou webcam.

Para arquivo, apenas modifique o nome do arquivo, para usar sua webcam, altere para um inteiro que irá indicar o índice de sua webcam.

> (Normalmente, se há apenas uma câmera, basta utilizar o valor 0).

## Alterando a área de interesse

Adicione o argumento _-r_ ou *--region_of_interest*

> Altere essas variáveis para definir área de interesse.

Definindo o início e fim (em x e y) de sua área de interesse.
(start_x, start_y, end_x, end_y)

## Alterando os modelos pré-treinados do YOLO

Adicione o argumento _-cfg_ ou *--model_cfg* para alterar o arquivo de configuração da rede YOLOv3
Adicione o argumento _-w_ ou *--model_weights* para alterar o arquivo de pesos da rede YOLOv3
Adicione o argumento _-s_ ou *--scale* para alterar a escala da rede YOLOv3

Este repositório já baixa as configurações e pesos para _320_.

Para mais detalhes e downloads de redes pré-treinadas, consulte [YOLO](https://pjreddie.com/darknet/yolo/).

## Alterando a tolerância das detecções

Adicione o argumento _-ct_ ou *--confidence_threshold* para alterar a tolerância de confiabilidade das detecções
Adicione o argumento _-nms_ ou *--nms_threshold* para alterar a tolerância de caixas limitantes sobrepostas
