from django.urls import path
from apps.transaccion import views

app_name='transaccion'

urlpatterns=[
    path('',views.transaccion,name='transacciones'),
    path('compra_inventario',views.compra_inventario,name='compra_inv'),
    path('devolucion_sobre_compra',views.devolucion_compra,name='dev_compra'),
]