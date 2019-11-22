from django.shortcuts import render
from apps.periodo.models import *
from django.shortcuts import redirect
import datetime, time 
from apps.contabilidad_costos.peps import * 
from apps.contabilidad_general.models import * 
from apps.periodo.forms import NotaForms

# Create your views here.
def resetear_saldos():
	cuenta_h=CuentaHija.objects.all()

	for hija in cuenta_h:
		hija.debe = hija.saldo_deudor_cuenta
		hija.haber = hija.saldo_acreedor_cuenta

		hija.saldo_acreedor_cuenta = 0.0
		hija.saldo_deudor_cuenta = 0.0



def sumar(request):
	cuenta_h=CuentaHija.objects.all()
	cuenta_p=Cuenta.objects.all()

	for hija in cuenta_h:
		saldo=hija.debe-hija.haber
		if saldo>0:
			hija.saldo_deudor_cuenta=saldo
			hija.save()
		else:
			hija.saldo_acreedor_cuenta=abs(saldo)
			hija.save()

	for padre in cuenta_p:
		for hija in cuenta_h:
			if padre.codigo_cuenta==hija.codigo_padre:
				padre.debe += hija.saldo_deudor_cuenta
				padre.haber += hija.saldo_acreedor_cuenta
				padre.save()

	for padre in cuenta_p:
		saldo=padre.debe-padre.haber
		if saldo>0:
			padre.saldo_deudor_cuenta=saldo
			padre.save()
		else:
			padre.saldo_acreedor_cuenta=abs(saldo)
			padre.save()

def cerrar_periodo(request, periodo_id):
	cuenta_p = Cuenta.objects.all()
	cuenta_h = CuentaHija.objects.all()
	periodo = Periodo.objects.get(id=periodo_id)
	
	sumar(request)

	i=0
	while i<len(cuenta_p):
		bp=BalancePeriodo()
		if i<len(cuenta_h):
			bp.hija_balance=cuenta_h[i]
			bp.saldo_deudor_h=cuenta_h[i].saldo_deudor_cuenta
			bp.saldo_acreedor_h=cuenta_h[i].saldo_acreedor_cuenta
		bp.periodo_balance=periodo
		bp.cuenta_balance=cuenta_p[i]
		bp.saldo_deudor=cuenta_p[i].saldo_deudor_cuenta
		bp.saldo_acreedor=cuenta_p[i].saldo_acreedor_cuenta
		bp.save()
		i+=1

def  periodo_contable ( request ):
	cant = 0
	periodos = Periodo.objects.all()
	for periodo in periodos:
		if periodo.estado_periodo == False:
			cant += 1

	if request.method == 'POST':
		if 'idPeriodo' in request.POST:
			idP = request.POST.get('idPeriodo')
			cerrar_periodo(request, idP)
			periodoCerrado = Periodo.objects.get(id =idP)
			periodoCerrado.estado_periodo = True # se indica que el periodo ha finalizado completamente
			periodoCerrado.final_periodo = time.strftime("%Y-%m-%d")
			periodoCerrado.periodo_ajuste=False # se indica que el proceso de ajuste a finalizado
			periodoCerrado.save()
			resetear_saldos()
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
			idPeriodo = 1
			fecha = time.strftime("%Y-%m-%d")
			id_cuenta = 19
			cant = 50
			precio_u = 1.10
			tipo = False
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
		cuentas = sumarMayor()
	else:
		cuentas = BalancePeriodo.objects.filter(periodo_balance = periodoActual)
	contexto = {
	'periodoActual' : periodoActual,
	'cuentas': cuentas,
	}

	return render (request, 'periodos/libro_mayor.html' , contexto)

def sumarMayor():
	cuenta_h=CuentaHija.objects.all()
	cuenta_p=Cuenta.objects.all()

	for hija in cuenta_h:
		saldo=hija.debe-hija.haber
		if saldo>0:
			hija.saldo_deudor_cuenta=saldo
		else:
			hija.saldo_acreedor_cuenta=abs(saldo)

	padre.debe = 0
	padre.haber = 0
	for padre in cuenta_p:
		for hija in cuenta_h:
			if padre.codigo_cuenta==hija.codigo_padre:
				padre.debe += hija.saldo_deudor_cuenta
				padre.haber += hija.saldo_acreedor_cuenta

	for padre in cuenta_p:
		saldo=padre.debe-padre.haber
		padre.debe = round(padre.debe,2)
		padre.haber = round(padre.haber,2)
		if saldo>0:
			padre.saldo_deudor_cuenta=round(saldo,2)
		else:
			padre.saldo_acreedor_cuenta=round(abs(saldo),2)
	return cuenta_p


	