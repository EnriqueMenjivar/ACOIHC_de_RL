from django.urls import path
from apps.contabilidad_costos.views import *

urlpatterns = [
    
    path('programaciones_lista/', programacion_list, name="programaciones_lista"),
    path('programaciones_nueva/', programacion_nueva, name="programaciones_nueva"),
    path('transacciones_programacion/', TransaccionesProgramacion.as_view()),
    path('seguimiento/(¿P<id_programacion>\d+)/', seguimiento, name="seguimiento"),
    path('detalles/(¿P<id_programacion>\d+)/', ver_detalles, name="detalles"),
    path('detalles_proceso/(¿P<id_proceso>\d+)/', ver_detalles_proceso, name="detalles_proceso"),
    path('empleado_lista/', Lista_Empleados.as_view(), name= "empleado_lista"),
    path('empleado_registrar/', registra_Empleado, name= 'empleado_registrar'),
    path('empleado_general/', planilla_general.as_view(), name= 'empleado_general'),
    path('empleado_planilla/<id>/', planilla_empleado , name = 'empleado_planilla'),
    path('lista_kardex/', lista_kardex, name= 'lista_kardex'),
    path('lista_kardex/kardex/<id>/', kardex, name= 'kardex'),
   
]

