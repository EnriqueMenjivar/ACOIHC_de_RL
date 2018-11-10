from django.urls import path
from apps.periodo.views import *

urlpatterns = [
    
    path('', periodo_contable, name="periodo_contable"),
    path('menu/<id>/', periodo_menu_vista , name="periodo_menu_vista"),
    path('estados/', periodo_menu_estados , name="periodo_menu_estados"),
]
