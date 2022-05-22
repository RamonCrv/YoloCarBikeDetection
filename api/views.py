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
def analyze(request):
    model = Deteccao
    template_name = 'base.html'
    context_object_name = 'transactions'
    paginate_by = 10
    queryset = Deteccao.objects.filter(id = '2')

    context = super(listar_registros, self).get_context_data(**kwargs)
    context['itens'] = Treinamento.objects.filter(id__exact='2') 
    return context
    





        