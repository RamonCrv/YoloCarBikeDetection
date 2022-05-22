import os
import keras
import tensorflow
from django.apps import AppConfig
from django.conf import settings
from tensorflow.keras.models import model_from_json

class VideoAppConfig(AppConfig):
    name = 'api'
    #name of your app

    #load your models and model weights here and these are linked     
    #"MODELS" variable that we mentioned in "settings.py"
    path = os.path.join(settings.MODELS, "your_model.h5") 
    path1 = os.path.join(settings.MODELS, 'model.json')

    json_file = open(path1, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    #loaded_model = model_from_json(loaded_model_json)
    #loaded_model.load_weights(path)