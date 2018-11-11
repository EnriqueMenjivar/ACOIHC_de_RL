from django.shortcuts import render
from apps.periodo.models import *
from django.shortcuts import redirect
import datetime, time 
from apps.contabilidad_costos.peps import * 

# Create your views here.
def  periodo_contable ( request ):
	cant = 0
	periodos = Periodo.objects.all()
	for periodo in periodos:
		if periodo.estado_periodo == False:
			cant += 1

	if request.method == 'POST':
		if 'idPeriodo' in request.POST:
			idP = request.POST.get('idPeriodo')
			periodoCerrado = Periodo.objects.get(id =idP)
			periodoCerrado.estado_periodo = True # se indica que el periodo ha finalizado completamente
			periodoCerrado.final_periodo = time.strftime("%Y-%m-%d")
			periodoCerrado.periodo_ajuste=False # se indica que el proceso de ajuste a finalizado
			periodoCerrado.save()
			return redirect('periodo_contable')
		if 'idPe' in request.POST:
			idP = request.POST.get('idPe')
			periodoCerrado = Periodo.objects.get(id =idP)
			periodoCerrado.periodo_ajuste=True #se indica que el proceso de ajuste esta vigente, mientras que el estado del periodo sigue activo
			periodoCerrado.save()
			return redirect('periodo_contable')
		if 'btnNuevo' in request.POST:
			objPeriodo = Periodo(inicio_periodo = time.strftime("%Y-%m-%d"), final_periodo = time.strftime("%Y-%m-%d"))
			objPeriodo.save()
			return redirect('periodo_contable')

	contexto = {
	'periodos' : periodos,
	'cant' :cant
	}
	return render (request, 'periodos/admin_periodos.html' , contexto)

def  periodo_menu_vista (request,id):
	periodoActual = Periodo.objects.get(id = id)
	contexto = {
	'periodoActual' : periodoActual,
	}
	return render (request, 'periodos/periodo_menu.html' , contexto)

def  periodo_menu_estados( request):
	periodoActual = Periodo.objects.get(id = 3)
	contexto = {
	'periodoActual' : periodoActual,
	}
	return render (request, 'periodos/periodo_estados.html' , contexto)





def  listar_transacciones( request):
	
	if request.method == 'POST':
		if 'btnPeps' in request.POST:
			idPeriodo = 1
			fecha = time.strftime("%Y-%m-%d")
			id_cuenta = 1
			cant = 80
			precio_u = 48.00
			tipo = True

			
			peps(idPeriodo, fecha,id_cuenta,cant,precio_u,tipo)
			ajuste_peps()
			return redirect('listar_transacciones')

	contexto = {
	'' : '',
	}
	return render (request, 'transaccion/listar_transacciones.html' , contexto)

