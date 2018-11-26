from django.urls import path
from apps.periodo.views import *

urlpatterns = [
    
    path('', periodo_contable, name="periodo_contable"),
    path('menu/<id>/', periodo_menu_vista , name="periodo_menu_vista"),
    path('estados/<id>/', periodo_menu_estados , name="periodo_menu_estados"),
    path('libro_mayor/<id>/', libro_mayor, name="libro_mayor"),
    path('transacciones/<id>/', listar_transacciones, name="listar_transacciones")
]
