from django.http import JsonResponse
from rest_framework.decorators import api_view
from pathlib import Path
import math
import os
from msilib.schema import ListView
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from api.models import Treinamento, Deteccao
from django.views.generic.list import ListView

from api.forms import UsuarioForm
from api.forms import UsuarioForm



# from scripts.gender_detection_class import GenderDetection
# from scripts.violence_detection_class import ViolenceDetection
# from scripts.violence_detection_against_woman_class import ViolenceDetectionAgainstWoman

# @api_view(["POST"])
# def analyze(request):

#     try:
#         request.FILES['video']
#     except KeyError:
#             json = "File called 'video' not found in Request!"
#     else:
#         video = request.FILES['video']
#         video_path = video.temporary_file_path()

#         extension =  os.path.splitext(video_path)[1]        

#         if(extension == '.avi'):
#             request.upload_handlers.pop(0)

#             tamanho = int(Path(video_path).stat().st_size/1024) #em KB

#             if(tamanho > 51200):
#                 json = "This video reached the maximum size. 50MB maximum size!"
#             else:
#                 violenceDAW = ViolenceDetectionAgainstWoman()
#                 json = violenceDAW.analize(video_path, request.data.get('type_detection'))         
#         else:
#             json = "This is not an allowed file type. Send a '.avi' video extension!"   
       
#     return JsonResponse(json, safe=False)




# Create your views here.
def CriarUsuario(request):
    form = UsuarioForm(request.POST)    
    if request.method == "POST":
        form = UsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            obj.save()
            return redirect('login')
    return render(request, 'usuarios/form.html', {'form':form})

 
class listar_registros(ListView):
    model = Deteccao
    template_name = 'base.html'
    context_object_name = 'transactions'
    paginate_by = 10
    queryset = Deteccao.objects.filter(id = '2')

    def get_context_data(self, **kwargs):
        context = super(listar_registros, self).get_context_data(**kwargs)
        context['itens'] = Treinamento.objects.filter(id__exact='2') 
        return context


        