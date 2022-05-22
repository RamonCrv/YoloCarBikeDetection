from django.urls import path
from django.contrib import admin
from api import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('analyze/', views.analyze)
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

