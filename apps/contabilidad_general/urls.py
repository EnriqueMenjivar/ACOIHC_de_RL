from django.urls import path, re_path
from apps.contabilidad_general import views

app_name = "contabilidad_general"

urlpatterns = [
	path('crear/', views.cuenta_create, name="crear"),
	path('crear-hija/<cuenta_id>/', views.cuenta_hija_create, name="crear-hija"),
	path('mostrar-cuentas/', views.catalogo_show, name="mostrar-cuentas"),
	path('mostrar-hijas/<cuenta_id>/', views.hijas_show, name="mostrar-hijas"),
	path('cuenta-editar/<cuenta_id>/', views.cuenta_update, name="cuenta-editar"),
	path('hija-editar/<hija_id>/', views.hija_update, name="hija-editar"),
	path('balance-comprobacion/<periodo_id>/', views.balance_comprobacion, name="balance-comprobacion"),
	path('estado-resultado/<periodo_id>/', views.estado_resultado, name="estado-resultado"),
	path('estado-capital/<periodo_id>/', views.estado_capital, name="estado-capital"),
	path('balance-general/<periodo_id>/', views.balance_general, name="balance-general"),
	path('ajax/load-agrupaciones/', views.load_agrupaciones, name="ajax"),
	path('prueba/<periodo_id>', views.cerrar_periodo, name="prueba"),
	path('sumar/', views.sumar, name="sumar"),
	#path('sumar1/', views.sumar1, name="sumar1"),
	
]
