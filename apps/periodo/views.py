from django.shortcuts import render
from apps.periodo.models import *
from django.shortcuts import redirect
import datetime, time 

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
			periodoCerrado.estado_periodo = True
			periodoCerrado.final_periodo = time.strftime("%Y-%m-%d")
			periodoCerrado.save()
			return redirect('periodo_contable')
		if 'btnNuevo' in request.POST:
			objPeriodo = Periodo(inicio_periodo = time.strftime("%Y-%m-%d"), final_periodo = time.strftime("%Y-%m-%d"), estado_periodo=False)
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