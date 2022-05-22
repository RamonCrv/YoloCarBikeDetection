from django.urls import path
from django.contrib import admin
from api import views

urlpatterns = [
    path('analyze/', views.analyze)
    
]
