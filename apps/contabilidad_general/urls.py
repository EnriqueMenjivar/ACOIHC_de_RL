from django.urls import path, re_path
from apps.contabilidad_general import views

app_name = "contabilidad_general"

urlpatterns = [
	#path('crear/', views.CuentaCreateView.as_view(), name="crear"),
	path('crear/', views.cuenta_create, name="crear"),
	path('crear_hija/<cuenta_id>/', views.cuenta_hija_create, name="crear_hija"),
	path('ajax/load-agrupaciones/', views.load_agrupaciones, name="ajax"),
	
]
