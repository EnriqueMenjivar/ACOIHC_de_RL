from django.shortcuts import render, HttpResponse
from apps.contabilidad_costos.models import *
from apps.periodo.models import Periodo
from apps.catalogo.models import Cuenta
from django.views.generic import TemplateView
from datetime import datetime
from django.core import serializers

def programacion_list(request):
	lista_programacion = Programacion.objects.all()
	return render(request,'contabilidad_costos/programacion_list.html', {'programaciones':lista_programacion})

def programacion_nueva(request):
	periodos = Periodo.objects.all()
	productos = Cuenta.objects.filter(codigo_padre='1141')
	materiales = Cuenta.objects.filter(codigo_padre='1143')
	cargos = Cargo.objects.all()
	contexto = {'periodos':periodos, 'productos':productos, 'materiales':materiales, 'cargos':cargos}
	return render(request, 'contabilidad_costos/programacion_nueva.html', contexto)

class ProgramacionesAjaxView(TemplateView):

	def get(self, request, *args, **kwargs):
		periodo = request.GET['periodo']
		periodoObject = Periodo.objects.get(id = periodo)
		fecha = request.GET['fecha']
		producto = request.GET['producto']
		productoNombre = Cuenta.objects.get(codigo_cuenta = producto).nombre_cuenta
		cantidad = request.GET['cantidad']
		programaciones = Programacion.objects.all().order_by('id')
		id_programacion =programaciones[len(programaciones) - 1].id + 1
		programacion = Programacion(id=id_programacion, periodo_programacion = periodoObject, fecha_programacion = fecha, producto_programacion = productoNombre, cantidad_programacion= int(cantidad))
		programacion.save()
		programacion_list = [programacion]
		data = serializers.serialize('json',programacion_list,fields = ('id'))
		return HttpResponse(data, content_type = 'application/json')
		
	


