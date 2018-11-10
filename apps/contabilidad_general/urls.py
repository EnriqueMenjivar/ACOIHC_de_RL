from django.urls import path, re_path
from apps.contabilidad_general import views

app_name = "contabilidad_general"

urlpatterns = [
	#path('crear/', views.CuentaCreateView.as_view(), name="crear"),
	path('crear/', views.cuenta_create, name="crear"),
	path('crear-hija/<cuenta_id>/', views.cuenta_hija_create, name="crear-hija"),
	path('mostrar-cuentas/', views.catalogo_show, name="mostrar-cuentas"),
	path('mostrar-hijas/<cuenta_id>/', views.hijas_show, name="mostrar-hijas"),
	path('cuenta-editar/<cuenta_id>/', views.cuenta_update, name="cuenta-editar"),
	path('hija-editar/<hija_id>/', views.hija_update, name="hija-editar"),
	path('ajax/load-agrupaciones/', views.load_agrupaciones, name="ajax"),
	path('prueba/<periodo_id>', views.cerrar_periodo, name="prueba"),
	
]
