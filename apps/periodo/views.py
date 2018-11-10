from django.shortcuts import render
from apps.periodo.models import *

# Create your views here.
def  periodo_contable ( request ):
	periodos = Periodo.objects.all()
	contexto = {
	'periodos' : periodos,
	}
	return render (request, 'periodos/admin_periodos.html' , contexto)

def  periodo_menu_vista (request):
	periodoActual = Periodo.objects.get(id = 5)
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