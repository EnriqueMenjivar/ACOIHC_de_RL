from django.shortcuts import render
from apps.periodo.models import *
from django.shortcuts import redirect
import datetime, time 
from apps.contabilidad_costos.peps import * 
from apps.contabilidad_general.models import * 

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

def  periodo_menu_estados( request,id):
	periodoActual = Periodo.objects.get(id = id)
	contexto = {
	'periodoActual' : periodoActual,
	}
	return render (request, 'periodos/periodo_estados.html' , contexto)


def  listar_transacciones( request,id):
	listTransaccion = list() # creamos la lista que enviaremos al contexto
	list_interna = list() # me permitira guardar en la primera posicion la transaccion, y en la segunda posicion una lista de transaccion_cuenta
	cv = 0
	periodo_existe = Periodo.objects.filter(id = id).exists()
	if periodo_existe:
		periodo = Periodo.objects.get(id=id)
		transaccion_existe = Transaccion.objects.filter(periodo_transaccion = periodo).exists()
		if transaccion_existe:
			transacciones = Transaccion.objects.filter(periodo_transaccion = periodo) #traemos las transacciones del periodo en cuestion
			for transaccion in transacciones:
				list_interna.append(transaccion)
				detalle_existe = Transaccion_Cuenta.objects.filter(transaccion_tc= transaccion).exists()
				if detalle_existe:
					detalle_transacciones = Transaccion_Cuenta.objects.filter(transaccion_tc= transaccion)
					list_interna.append(detalle_transacciones)
				listTransaccion.append(list_interna)
				list_interna = []

	if request.method == 'POST': #Prueba para el metodo pesp
		if 'btnPeps' in request.POST:
			idPeriodo = 3
			fecha = time.strftime("%Y-%m-%d")
			id_cuenta = 7
			cant = 30
			precio_u = 9
			tipo = True
			cv = list()
			cv = peps(idPeriodo,fecha,id_cuenta,cant,precio_u,tipo,cv)
			for x in cv:
				print(x[0])
				print(x[1])
				print(x[2])
			return redirect('listar_transacciones', id = id)

	contexto = {
	'listTransaccion' : listTransaccion
	}
	return render (request, 'transaccion/listar_transacciones.html' , contexto)

def  libro_mayor( request,id):
	periodoActual = Periodo.objects.get(id = id)
	if periodoActual.estado_periodo == False:
		cuentas = Cuenta.objects.all()
	else:
		cuentas = BalancePeriodo.objects.filter(periodo_balance = periodoActual)
	contexto = {
	'periodoActual' : periodoActual,
	'cuentas': cuentas,
	}
	return render (request, 'periodos/libro_mayor.html' , contexto)