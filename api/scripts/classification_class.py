
import os
import cv2
import cvlib
import numpy as np
import pandas as pd
import time
import glob
import requests
import uuid
import boto3

import cloudinary
import cloudinary.uploader
import cloudinary.api

from scripts.car_detection_class import CarDetection
from scripts.belt_detection_class import BeltDetection
import imutils
import logging

class Classification():
  def __init__(self ):
    self.server = "http://127.0.0.1:8000"
    self.export_frames = False
    self.export_video = True
    self.acuracy=0.9
    self.detect_belt = True
    self.driver_detected = False
    self.unbelted_driver = False
    self.passenger_detected = False
    self.unbelted_passenger = False
  
    self.carDetection = CarDetection()
    self.beltDetection = BeltDetection()   

  
  def analize(self, filename, type_detection):
    print('Carregando o Vídeo...')
    millis = time.time()

    if type_detection == 'belt':
      self.detect_belt = True

    vs = cv2.VideoCapture(filename)
    
    fps = vs.get(cv2.CAP_PROP_FPS)
    frame_count = int(vs.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count/fps


    print('Enviando o Vídeo para Detecção...')
    unbelted_seconds, ary_images,ary_names, url_video = self.detectation_from_video(vs, frame_count, fps)
    
    millis2 = time.time()

    print('Resultado do Vídeo:')
    
    retorno = { 
      'driver_detected': self.driver_detected,
      'unbelted_driver': self.unbelted_driver,
      'passenger_detected': self.passenger_detected,
      'unbelted_passenger': self.unbelted_passenger,
      'fps': round(fps),
      'frame_count': frame_count,
      'duration': round(duration,2),
      'unbelted_seconds': unbelted_seconds,
      'processing_time': round(millis2-millis, 3),
      'unbelted_name': ary_names,
      'url_frames': ary_images,
      'url_video': url_video
    }
    return retorno

  def detectation_from_video(self, vs, frame_count, fps):
    # video info
    video_format = '.webm'
    video_id = str(uuid.uuid1()) + video_format    

    output_video = "static/inputs/" + video_id
    print("Analisando Video: "+output_video)

    writer = None

    #config
    frame_seq = 0
    size = 128
    frame_rate = 1
    frame_jump = 12

    #return
    unbelted_seconds = []
    ary_images = []
    ary_names = []

    export_video_frame = False

    
    while frame_seq < frame_count:      

      vs.set(cv2.CAP_PROP_POS_FRAMES,frame_seq)

      # read the next frame from the file
      (grabbed, image) = vs.read()
      copy_frame = image.copy()
      frame = imutils.resize(copy_frame, width=min(640, copy_frame.shape[1]))
      (H, W) = frame.shape[:2]

      # if the frame was not grabbed, then we have reached the end of the stream
      if not grabbed:
        break

      if writer is None:
        fourcc = cv2.VideoWriter_fourcc(*"vp80")
        #writer = cv2.VideoWriter(output_video, fourcc, 30, (W, H), True)
        writer = cv2.VideoWriter(output_video, fourcc, 30, (W, H))

      # analyze only 2 frames per second
      if frame_seq % frame_jump == 0:
        print("\n\n[ETAPA] Analisando Frame: "+str(frame_seq)+"")

        # call belt detection
        if self.detect_belt == True:

          print("[ETAPA] Procurando Carro no Frame....")
          cars = self.carDetection.detectCar(frame)
          if len(cars) > 0 :
            print("[RESULTADO] "+str(len(cars))+" Carro(s) encontrado(s) no tempo: "+str(frame_seq / fps)+".")
          else:
             print("[RESULTADO] Nenhum Carro Detectado.")
          if(cars):
            print("[ETAPA] Procurando Motorista e Passageiro...")
            for car in cars:
              
              uuid_detection = str(uuid.uuid1())

              #PROCURANDO MOTORISTA
              driverDetected, driverImg = self.carDetection.detectDriver(frame, car, frame_seq / fps)
              if(driverDetected):              
                self.driver_detected = True
                print("[RESULTADO] Motorista Encontrado no tempo: "+str(frame_seq / fps)+"")            
                print("[ETAPA] Verificando Cinto no Motorista...")
                
                if(self.beltDetection.detectUnbeltedDriver(driverImg) == True):
                  self.unbelted_driver = True
                  unbelted_seconds.append(frame_seq / fps)
                  ary_names.append('driver')                
                  
                  #salva a imagem
                  img_path = "static/outputs/Persons/unbelted/driver_" + uuid_detection + ".png"
                  cv2.imwrite(img_path, driverImg)             
                  ary_images.append(self.server+"/"+img_path)             
                  print("[RESULTADO] Motorista Sem Cinto Encontrado no tempo: "+str(frame_seq / fps)+".")
                else:
                  #salva a imagem
                  img_path = "static/outputs/Persons/belted/driver_" + uuid_detection + ".png"
                  cv2.imwrite(img_path, driverImg)             
                  ary_images.append(self.server+"/"+img_path)  
                  print("[RESULTADO] Motorista Com Cinto Encontrado no tempo: "+str(frame_seq / fps)+".")
              
              else:
                 print("[RESULTADO] Motorista Não detectado.")       
              
              
              #PROCURANDO PASSAGEIRO            
              passengerDetected, passengerImg = self.carDetection.detectPassenger(frame, car, frame_seq / fps)
              if(passengerDetected):            
                self.passenger_detected = True
                print("[RESULTADO] Passageiro encontrado no tempo: "+str(frame_seq / fps)+".")          
                print("[ETAPA] Verificando Cinto no passageiro.")
                
                if(self.beltDetection.detectUnbeltedPassenger(passengerImg) == True):
                  self.unbelted_passenger = True
                  unbelted_seconds.append(frame_seq / fps)
                  ary_names.append('passenger')    

                  #salva a imagem
                  img_path = "static/outputs/Persons/unbelted/passenger_" + uuid_detection + ".png"
                  cv2.imwrite(img_path, passengerImg)             
                  ary_images.append(self.server+"/"+img_path)  
                  print("[RESULTADO] Passageiro Sem Cinto Encontrado no tempo:"+str(frame_seq / fps)+".")    
                else:                  
                  #salva a imagem
                  img_path = "static/outputs/Persons/belted/passenger_" + uuid_detection + ".png"
                  cv2.imwrite(img_path, passengerImg)                     
                  ary_images.append(self.server+"/"+img_path)  
                  print("[RESULTADO] Passageiro Com Cinto Encontrado no tempo: "+str(frame_seq / fps)+".")
              
              else:
                 print("[RESULTADO] Passageiro Não detectado.")   

      else: 

        if self.unbelted_driver == True or self.unbelted_passenger == True :
          label = 'Foram Encontrados usuarios sem Cinto.'
        else:
          label = 'Nenhum Usuário sem cinto foi localizado.'

        text = ""
        # text = " Analise: {}".format(label)
        if self.detect_belt == True:
          cv2.putText(frame, text, (35, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)

      # write the frame to disk
      # if self.export_video == True:
      writer.write(frame)

      frame_seq += frame_rate

    if self.export_video:
      writer and writer.release()
      
      # save video at S3
      #self.s3.Bucket('ekma').upload_file(Filename=output_video, Key=video_id, ExtraArgs={'ACL': 'public-read', 'ContentType': "video/avi"})


      # cloudinary.config( 
      #   cloud_name = "dh6fx8j1d", 
      #   api_key = "129264633655466", 
      #   api_secret = "7xmWuIIUE3nRXTV2zfKyAuUcZ2Y",
      #   secure = True
      # )

      #save video at cloudinary
      # cloudinary.uploader.upload(output_video, public_id = video_id)


      #return_cloudinary = cloudinary.uploader.upload_large(output_video, resource_type = "video", public_id = video_id)

      # remove file
      #os.remove(output_video)
    
    cv2.destroyAllWindows()

    #url_video = return_cloudinary
    url_video = self.server+'/static/inputs/' + video_id

    return unbelted_seconds, ary_images, ary_names, url_video
