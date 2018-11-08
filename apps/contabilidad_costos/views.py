from django.shortcuts import render
from apps.contabilidad_costos.models import *

def programacion_list(request):
	lista_programacion = Programacion.objects.all()
	return render(request,'contabilidad_costos/programacion_list.html', {'programaciones':lista_programacion})

def programacion_nueva(request):
	return render(request, 'contabilidad_costos/programacion_nueva.html')


