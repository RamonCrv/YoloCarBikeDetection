from django.http import JsonResponse
from rest_framework.decorators import api_view
from pathlib import Path
import math
import os
from msilib.schema import ListView
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
#from api.models import Treinamento, Deteccao
from django.views.generic.list import ListView

from scripts.classification_class import Classification
from scripts.car_detection_class import CarDetection
from scripts.belt_detection_class import BeltDetection
# from scripts.violence_detection_against_woman_class import ViolenceDetectionAgainstWoman

@api_view(["POST"])
def analyze(request):
    try:
        request.FILES['video']
    except KeyError:
            json = "File called 'video' not found in Request!"
    else:
        video = request.FILES['video']
        video_path = video.temporary_file_path()        
        extension =  os.path.splitext(video_path)[1]        

        if(extension == '.mp4' or extension == '.avi' or extension == '.MOV'):
            request.upload_handlers.pop(0)
            tamanho = int(Path(video_path).stat().st_size/1024) #em KB
            if(tamanho > 512000):
                json = "This video reached the maximum size. 50MB maximum size!"
            else:
                classification = Classification()
                json = classification.analize(video_path, request.data.get('type_detection'))         
        else:
            json = "This is not an allowed file type. Send a '.avi' video extension!"  
                   
    return JsonResponse(json, safe=False)





        