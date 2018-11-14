from django.urls import path
from apps.periodo.views import *

urlpatterns = [
    
    path('', periodo_contable, name="periodo_contable"),
    path('menu/<id>/', periodo_menu_vista , name="periodo_menu_vista"),
    path('estados/<id>/', periodo_menu_estados , name="periodo_menu_estados"),
    path('transacciones/<id>/', listar_transacciones, name="listar_transacciones")#la cree para hacer pruebas
]
