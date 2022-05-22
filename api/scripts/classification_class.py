
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
    print('reading video...')
    millis = time.time()

    if type_detection == 'belt':
      self.detect_belt = True

    vs = cv2.VideoCapture(filename)
    
    fps = vs.get(cv2.CAP_PROP_FPS)
    frame_count = int(vs.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count/fps


    print('sending video to detection...')
    unbelted_seconds, ary_images,ary_names, url_video = self.detectation_from_video(vs, frame_count, fps)
    
    millis2 = time.time()

    print('video result:')
    
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
    video_format = '.avi'
    video_id = str(uuid.uuid1()) + video_format    

    output_video = "static/inputs/" + video_id
    print("Analisando Video: "+output_video)

    writer = None

    unbelted_seconds = []
    frame_seq = 0
    size = 128
    frame_rate = 1
    frame_jump = 30
    ary_images = []
    ary_names = []

    export_video_frame = False
    
    while frame_seq < frame_count:

      print("Frame: "+str(frame_seq))

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
        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        writer = cv2.VideoWriter(output_video, fourcc, 30,
          (W, H), True)

      # analyze only 2 frames per second
      if frame_seq % frame_jump == 0:

        # call belt detection
        if self.detect_belt == True:

          print("Procurando Carro")
          if(self.carDetection.detectCar(frame) == True):            
            print("Carro Encontrado")
            
            print("Procurando Motorista")            
            if(self.carDetection.detectDriver(frame) == True):              
              self.driver_detected = True
              print("Motorista Encontrado")
            
              print("Verificando Cinto")
              if(self.beltDetection.detectUnbeltedDriver(frame) == True):
                self.unbelted_driver = True
                unbelted_seconds.append(frame_seq / fps)
                ary_names.append('driver')                
                print("Motorista Sem Cinto")
            
            print("Procurando Passageiro") 
            if(self.carDetection.detectPassenger(frame) == True):            
              self.passenger_detected = True
            
              print("Verificando Cinto")
              if(self.beltDetection.detectUnbeltedPassenger(frame) == True):
                self.unbelted_passenger = True
                unbelted_seconds.append(frame_seq / fps)
                ary_names.append('passenger')          
                print("Passageiro Sem Cinto")

            # write the frame
            image_path = 'static/outputs/frames/frame_'+str(frame_seq) + '.jpg'
            cv2.imwrite(image_path, frame)
            
            # upload file to S3
            image_id = str(uuid.uuid1()) + '.jpg'

            # SALVANDO O CORTE DO CARRO E
            cv2.imwrite("static/outputs/frames/car_" + image_id, frame)

            if export_video_frame == False:
              export_video_frame = True
            
            # remove file
            os.remove(image_path)

      else: 

        if self.unbelted_driver == True or self.unbelted_passenger == True :
          label = 'Foram Encontrados usuarios sem Cinto.'
        else:
          label = 'Nenhum Usuário sem cinto foi localizado.'

        text = " Analise: {}".format(label)
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
        
      # remove file
      #os.remove(output_video)
    
    cv2.destroyAllWindows()

    url_video = self.server+'/static/inputs/' + video_id

    return unbelted_seconds, ary_images, ary_names, url_video
