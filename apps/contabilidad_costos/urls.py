from django.urls import path
from apps.contabilidad_costos.views import *

urlpatterns = [
    
    path('programaciones_lista/', programacion_list, name="programaciones_lista"),
    path('programaciones_nueva/', programacion_nueva, name="programaciones_nueva"),
    path('programaciones_ajax/', ProgramacionesAjaxView.as_view()),
    path('empleado_lista/', Lista_Empleados.as_view(), name= "empleado_lista"),
    path('empleado_registrar/', Registra_Empleado.as_view(), name= 'empleado_registrar'),
    path('empleado_general/', planilla_general, name= 'empleado_general'),
   
]