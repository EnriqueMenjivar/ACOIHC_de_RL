from django.urls import path
from apps.contabilidad_costos.views import *

urlpatterns = [
    
    path('programaciones_lista/', programacion_list, name="programaciones_lista"),
    path('programaciones_nueva/', programacion_nueva, name="programaciones_nueva"),
    path('programaciones_ajax/', ProgramacionesAjaxView.as_view()),
]