from django.urls import path
from apps.transaccion import views

app_name='transaccion'

urlpatterns=[
    path('',views.transaccion,name='transacciones'),
    path('compra_inventario',views.compra_inventario,name='compra_inv'),
    path('devolucion_sobre_compra',views.devolucion_compra,name='dev_compra'),
    path('venta',views.venta,name='venta'),
    path('compra_tangibles',views.compra_tangibles,name='compra_tangibles'),
    path('venta_tangibles',views.venta_tangibles,name='venta_tangibles'),
]