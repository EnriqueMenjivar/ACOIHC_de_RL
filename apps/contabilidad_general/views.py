from django.shortcuts import render, redirect, render_to_response
from django.urls import reverse_lazy
from apps.catalogo.forms import CuentaForm, AgrupacionForm, HijaForm
from apps.catalogo.models import Grupo, Agrupacion, Cuenta, CuentaHija
from apps.periodo.models import BalancePeriodo, Periodo, NotaPeriodo
from apps.periodo.models import BalancePeriodo, Periodo
from apps.contabilidad_general.models import *
from django.views.generic import ListView, CreateView, UpdateView
from django.http import HttpResponse 
from django.db.models import Q
from django.template import RequestContext
from apps.periodo.models import NotaPeriodo, Periodo

# Create your views here.

def cuenta_create(request):
	grupos = Grupo.objects.all()

	if request.method=='POST':
		cuenta = Cuenta()
		ultima_cuenta = Cuenta.objects.latest("id");
		agrupaciones = Cuenta.objects.filter(agrupacion=request.POST['agrupacion']).order_by('codigo_cuenta')
		codigo = agrupaciones[len(agrupaciones)-1].codigo_cuenta+1

		if(ultima_cuenta):
			cuenta.id = ultima_cuenta.id+1

		cuenta.agrupacion = Agrupacion.objects.get(id=request.POST['agrupacion'])
		cuenta.nombre_cuenta = request.POST['nombre_cuenta']
		cuenta.descripcion_cuenta = request.POST['descripcion_cuenta']
		cuenta.codigo_cuenta = codigo
		cuenta.save()

		return redirect('contabilidad_general:mostrar-cuentas')
	return render(request, 'contabilidad_general/cuenta_create.html', {'grupos':grupos, })
	
def load_agrupaciones(request):
	grupo_id = request.GET.get('grupo')
	agrupaciones = Agrupacion.objects.filter(codigo_grup=grupo_id).order_by('nombre_agrupacion')
	return render(request, 'contabilidad_general/dropdown_opcions.html', {'agrupaciones':agrupaciones,})

def cuenta_hija_create(request, cuenta_id):

	if request.method=='POST':
		cuenta_hija = CuentaHija()
		ultima_cuenta_h = CuentaHija.objects.latest("id")
		cuenta_p = Cuenta.objects.get(id=cuenta_id)
		cuenta_h = CuentaHija.objects.filter(padre=cuenta_id).order_by('codigo_cuenta')
		
		if cuenta_h:
			cod_cuenta_h=cuenta_h[len(cuenta_h)-1].codigo_cuenta+1
		else:
			cod_cuenta_h = str(cuenta_p.codigo_cuenta)+str(0)+str(1)
		
		if(ultima_cuenta_h):
			cuenta_hija.id = ultima_cuenta_h.id + 1
		cuenta_hija.padre = cuenta_p
		cuenta_hija.codigo_padre = cuenta_p.codigo_cuenta
		cuenta_hija.nombre_cuenta = request.POST['nombre_cuenta']
		cuenta_hija.codigo_cuenta = cod_cuenta_h
		cuenta_hija.descripcion_cuenta = request.POST['descripcion_cuenta']
		cuenta_hija.saldo_deudor = 0.0
		cuenta_hija.saldo_acreedor = 0.0

		cuenta_hija.save()

		return redirect('contabilidad_general:mostrar-cuentas')
	return render(request, 'contabilidad_general/cuenta_hija_create.html')

def catalogo_show(request):
	cuentas = Cuenta.objects.all().order_by('codigo_cuenta')
	return render(request, 'contabilidad_general/catalogo_show.html', {'cuentas':cuentas})

def hijas_show(request, cuenta_id):
	hijas = CuentaHija.objects.filter(padre=cuenta_id).order_by('id')
	return render(request, 'contabilidad_general/hijas_show.html', {'hijas':hijas,})

def cuenta_update(request, cuenta_id):
	grupos = Grupo.objects.all()

	cuenta = Cuenta.objects.get(id=cuenta_id)
	if request.method == 'GET':
		form = CuentaForm(instance=cuenta)
	else:
		form = CuentaForm(request.POST, instance=cuenta)
		if form.is_valid():
			form.save()
		return redirect('contabilidad_general:mostrar-cuentas')
	contexto = {
		'form':form,
		'cuenta':cuenta,
		'grupos': grupos,
	}
	return render(request, 'contabilidad_general/cuenta_update.html', contexto)

def hija_update(request, hija_id):
	hija = CuentaHija.objects.get(id=hija_id)
	if request.method == 'GET':
		form = HijaForm(instance=hija)
	else:
		form = HijaForm(request.POST, instance=hija)
		if form.is_valid():
			form.save()
		return redirect('contabilidad_general:mostrar-cuentas')
	contexto = {
		'form':form,
		'hija':hija,
	}
	return render(request, 'contabilidad_general/hija_update.html', contexto)

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
	if 'btnCerrarPeriodo' in request.POST:
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
	return render(request, 'contabilidad_general/prueba.html', {'periodo_id':periodo_id})

def balance_comprobacion(request, periodo_id):
	balances = BalancePeriodo.objects.filter(periodo_balance=periodo_id)
	fecha_0=balances[0].periodo_balance.inicio_periodo
	fecha_1=balances[0].periodo_balance.final_periodo
	acreedor=0
	deudor=0
	mensaje=''
	context = {''}
	

	for balance in balances:
		acreedor += balance.saldo_acreedor
		deudor += balance.saldo_deudor

	acreedor = round(acreedor, 2)
	deudor = round(deudor, 2)
	if acreedor==deudor:
		mensaje='Se cumple partida doble'
	else:
		mensaje='No se cumple partida doble'


	estado=False
	p = Periodo.objects.get(id=1)

	if request.method=='POST':
		nota = NotaPeriodo()
		nota.titulo_nota=request.POST['titulo']
		nota.descripcion_nota=request.POST['descripcion']
		nota.periodo_nota= p
		nota.save()
		estado = True

		notas = NotaPeriodo.objects.all()
		context = {
			'notas' : notas,
		}

		return render(request, 'contabilidad_general/notas_list.html', context)
	else:
		context={
			'balances':balances,
			'acreedor': acreedor,
			'deudor': deudor,
			'mensaje': mensaje,
			'fecha_inicio': fecha_0,
			'fecha_final': fecha_1,
			'periodo':Periodo,
			'estado': estado,
		}

		return render(request, 'contabilidad_general/balance_comprobacion.html', context)

def notas_list(request):
	notas = NotaPeriodo.objects.all()
	contexto1 = {'notas' : notas}

	return render(request, 'contabilidad_general/notas_list.html', context)


def estado_resultado(request, periodo_id):
	balances = BalancePeriodo.objects.filter(Q(periodo_balance=periodo_id), 
											Q(cuenta_balance__agrupacion__codigo_agrupacion=41)|
											Q(cuenta_balance__agrupacion__codigo_agrupacion=51)|
											Q(cuenta_balance__agrupacion__codigo_agrupacion=61)).\
											order_by('-cuenta_balance__nombre_cuenta')
	fecha_0=balances[0].periodo_balance.inicio_periodo
	fecha_1=balances[0].periodo_balance.final_periodo
	ingresos=0
	gastos=0
	context = {''}

	for balance in balances:
		gastos += balance.saldo_deudor
		ingresos += balance.saldo_acreedor

	utilidad_periodo = ingresos-gastos

	estado=False
	p = Periodo.objects.get(id=periodo_id)
	
	if request.method=='POST':
		nota = NotaPeriodo()
		nota.titulo_nota=request.POST['titulo']
		nota.descripcion_nota=request.POST['descripcion']
		nota.periodo_nota= p
		nota.save()
		estado = True

		notas = NotaPeriodo.objects.all()
		context = {
			'notas' : notas,
		}

		return render(request, 'contabilidad_general/notas_list.html', context)
	else:

		context = {
			'balances': balances,
			'ingresos': round(ingresos,2),
			'gastos': round(gastos,2),
			'utilidad_periodo':round(utilidad_periodo,2),
			'fecha_inicio': fecha_0,
			'fecha_final': fecha_1,
			'estado': estado,
		}
		return render(request, 'contabilidad_general/estado_resultado.html', context)

def utilidad_periodo(request, periodo_id):
	balances = BalancePeriodo.objects.filter(Q(periodo_balance=periodo_id), 
											Q(cuenta_balance__agrupacion__codigo_agrupacion=41)|
											Q(cuenta_balance__agrupacion__codigo_agrupacion=51)|
											Q(cuenta_balance__agrupacion__codigo_agrupacion=61))
	ingresos=0
	gastos=0

	for balance in balances:
		gastos += balance.saldo_deudor
		ingresos += balance.saldo_acreedor

	return round(ingresos-gastos,2)
	
def estado_capital(request, periodo_id):
	balances = BalancePeriodo.objects.filter(Q(periodo_balance=periodo_id), 
											Q(cuenta_balance__agrupacion__codigo_agrupacion__startswith=3)).\
											order_by('cuenta_balance__nombre_cuenta')
	fecha_0=balances[0].periodo_balance.inicio_periodo
	fecha_1=balances[0].periodo_balance.final_periodo
	inversiones=utilidad_periodo(request, periodo_id)
	desinversiones=0
	utilidad_p=inversiones
	context = {''}

	for balance in balances:
		inversiones += balance.saldo_acreedor
		desinversiones += balance.saldo_deudor

	capital_social = inversiones-desinversiones

	estado=False
	p = Periodo.objects.get(id=1)
	
	if request.method=='POST':
		nota = NotaPeriodo()
		nota.titulo_nota=request.POST['titulo']
		nota.descripcion_nota=request.POST['descripcion']
		nota.periodo_nota= p
		nota.save()
		estado = True

		notas = NotaPeriodo.objects.all()
		context = {
			'notas' : notas,
		}

		return render(request, 'contabilidad_general/notas_list.html', context)
	else:

		context = {
			'balances':balances,
			'inversiones': round(inversiones,2),
			'desinversiones': round(desinversiones,2),
			'capital_social': round(capital_social,2),
			'utilidad_periodo':utilidad_p,
			'fecha_inicio': fecha_0,
			'fecha_final': fecha_1,
			'estado' : estado,
		}

		return render(request, 'contabilidad_general/estado_capital.html', context)

def capital_social(request, periodo_id):
	balances = BalancePeriodo.objects.filter(Q(periodo_balance=periodo_id), 
											Q(cuenta_balance__agrupacion__codigo_agrupacion__startswith=3))
	inversiones=utilidad_periodo(request, periodo_id)
	desinversiones=0
	utilidad_p=inversiones

	for balance in balances:
		inversiones += balance.saldo_acreedor
		desinversiones += balance.saldo_deudor

	return round(inversiones-desinversiones,2)

def balance_general(request, periodo_id):
	balances = BalancePeriodo.objects.filter(Q(periodo_balance=periodo_id), 
											Q(cuenta_balance__agrupacion__codigo_agrupacion__startswith=1)|
											Q(cuenta_balance__agrupacion__codigo_agrupacion__startswith=2)).\
											order_by('cuenta_balance__agrupacion__codigo_agrupacion')
	fecha_1=balances[0].periodo_balance.final_periodo

	debe=0
	haber=capital_social(request, periodo_id)
	capital_s=haber
	mensaje=''
	context = {''}

	for balance in balances:
		haber += balance.saldo_acreedor
		debe += balance.saldo_deudor

	haber = round(haber, 2)
	debe = round(debe, 2)
	if debe==haber:
		mensaje='Se cumple dualidad económica'
	else:
		mensaje='No se cumple dualidad económica'


	estado=False
	p = Periodo.objects.get(id=1)
	
	if request.method=='POST':
		nota = NotaPeriodo()
		nota.titulo_nota=request.POST['titulo']
		nota.descripcion_nota=request.POST['descripcion']
		nota.periodo_nota= p
		nota.save()
		estado = True

		notas = NotaPeriodo.objects.all()
		context = {
			'notas' : notas,
		}

		return render(request, 'contabilidad_general/notas_list.html', context)
	else:

		context={
			'balances':balances,
			'debe': debe,
			'haber': haber,
			'capital_social': capital_s,
			'mensaje': mensaje,
			'fecha_final': fecha_1,
			'estado' : estado,
		}

		return render(request, 'contabilidad_general/balance_general.html', context)

def flujo_de_efectivo(request, periodo_id):
	total_entradas = 0.0
	total_salidas = 0.0
	
	balances = BalancePeriodo.objects.filter(periodo_balance=periodo_id).\
									  filter( 
											Q(cuenta_balance__codigo_cuenta=5101)|
											Q(cuenta_balance__codigo_cuenta=5102)|
											Q(cuenta_balance__codigo_cuenta=1109)|
											Q(cuenta_balance__codigo_cuenta=1104)|
											Q(cuenta_balance__codigo_cuenta=1105)|
											Q(cuenta_balance__codigo_cuenta=1106)|
											Q(cuenta_balance__codigo_cuenta=4102)|
											Q(cuenta_balance__codigo_cuenta=2105)|
											Q(cuenta_balance__codigo_cuenta=2107)|
											Q(cuenta_balance__codigo_cuenta=2108)|
											Q(cuenta_balance__codigo_cuenta=1201)|
											Q(cuenta_balance__codigo_cuenta=1202)|
											Q(cuenta_balance__codigo_cuenta=1204)|
											Q(cuenta_balance__codigo_cuenta=2101)|
											Q(cuenta_balance__codigo_cuenta=2201)).\
											order_by('cuenta_balance__agrupacion__codigo_agrupacion')

	fecha_inicio = balances[0].periodo_balance.inicio_periodo
	fecha_final = balances[0].periodo_balance.final_periodo

	for balance in balances:
		total_entradas += balance.saldo_deudor
		total_salidas += balance.saldo_acreedor

	total_salidas = round(total_salidas, 2)
	total_entradas = round(total_entradas, 2)

	estado=False
	p = Periodo.objects.get(id=1)
	
	if request.method=='POST':
		nota = NotaPeriodo()
		nota.titulo_nota=request.POST['titulo']
		nota.descripcion_nota=request.POST['descripcion']
		nota.periodo_nota= p
		nota.save()
		estado = True

		notas = NotaPeriodo.objects.all()
		context = {
			'notas' : notas,
		}

		return render(request, 'contabilidad_general/notas_list.html', context)
	else:
		context = {
			'fecha_inicio' : fecha_inicio,
			'fecha_final' : fecha_final,
			'total_entradas' : total_entradas,
			'total_salidas' : total_salidas,
			'saldo_final' : (total_entradas - total_salidas),
			'balances' : balances
		}
		return render (request, 'contabilidad_general/flujo_de_efectivo.html', context)

def ratios_financieros(request, periodo_id):
	balances = BalancePeriodo.objects.filter(periodo_balance=periodo_id)
	fecha_0=balances[0].periodo_balance.inicio_periodo
	fecha_1=balances[0].periodo_balance.final_periodo
	activo_corriente=0
	pasivo_corriente=0
	pasivo_no_corriente=0
	total_activo=0
	total_pasivo=0
	total_inventario=0
	capital=0
	ventas = 0
	utilidad= 0
	costo_de_venta = 0

	"""
	RAZONES DE LIQUIDEZ

	razón de liquidez corriente = activo corriente/pasivo corriente
	prueba acida = (activo corriente - inventario)/pasivo corriente

	RAZONES DE ENDEUDAMEINTO

	Razón entre deuda y capital = total pasivo/capital
	Razón entre deuda y activos totales = total pasivo/ total activo

	RAZON DE RENTABILIDAD

	Rentabilidad en relación con las ventas = (Ventas - Costo de venta)/Ventas
	Rentabilidad en relación con la inversión = (Utilidades)/ total activo
	"""

	#INICIANDO RESULTADOS
	prueba_de_liquidez = 0
	prueba_acida = 0
	deuda_capital = 0
	deuda_at = 0
	rentabilidad_ventas = 0
	rentabilidad_inversion = 0


	for balance in balances:
		#las cuentas que son activos
		if(balance.cuenta_balance.agrupacion.codigo_grup.codigo_grupo == '1'):
			total_activo += balance.saldo_deudor
			total_activo -= balance.saldo_acreedor
			#las cuentas que son de activo corriente
			if(balance.cuenta_balance.agrupacion.codigo_agrupacion == '11'):
				activo_corriente += balance.saldo_deudor
				activo_corriente -= balance.saldo_acreedor

				if(balance.cuenta_balance.codigo_cuenta == 1103  or
					balance.cuenta_balance.codigo_cuenta == 1104 or
					balance.cuenta_balance.codigo_cuenta == 1105 or
					balance.cuenta_balance.codigo_cuenta == 1106 ):
					total_inventario += balance.saldo_deudor
					total_inventario -= balance.saldo_acreedor
		#las cuentas que son pasivos
		if(balance.cuenta_balance.agrupacion.codigo_grup.codigo_grupo == '2'):
			total_pasivo -= balance.saldo_deudor
			total_pasivo += balance.saldo_acreedor
			#las cuentas que son de pasivo corriente
			if(balance.cuenta_balance.agrupacion.codigo_agrupacion == '21'):
				pasivo_corriente -= balance.saldo_deudor
				pasivo_corriente += balance.saldo_acreedor
			#las cuentas que son de pasivo no corriente
			if(balance.cuenta_balance.agrupacion.codigo_agrupacion == '22'):
				pasivo_no_corriente -= balance.saldo_deudor
				pasivo_no_corriente += balance.saldo_acreedor
		#Si la cuenta es de capital
		if(balance.cuenta_balance.agrupacion.codigo_grup.codigo_grupo == '3'):
			capital -= balance.saldo_deudor
			capital += balance.saldo_acreedor
			#Si la cuenta es de utilidades
			if(balance.cuenta_balance.codigo_cuenta == 3301):
				utilidad -= balance.saldo_deudor
				utilidad += balance.saldo_acreedor
		#Si la cuenta es la cuenta ventas
		if(balance.cuenta_balance.codigo_cuenta == 5101):
			ventas -= balance.saldo_deudor
			ventas += balance.saldo_acreedor
		#Si la cuenta es la cuenta costo de ventas
		if(balance.cuenta_balance.codigo_cuenta == 4104):
			costo_de_venta += balance.saldo_deudor
			costo_de_venta -= balance.saldo_acreedor
		
		#calculo
		if(pasivo_corriente != 0):
			prueba_de_liquidez = (activo_corriente)/(pasivo_corriente)
			prueba_acida = (activo_corriente - total_inventario)/(pasivo_corriente)
		if(capital != 0):
			deuda_capital = (total_pasivo)/capital
		if(total_activo !=0):
			deuda_at = (total_pasivo)/total_activo
			rentabilidad_inversion = (utilidad)/total_activo
		if(ventas !=0):
			rentabilidad_ventas = (ventas- costo_de_venta)/(ventas)




	context={
		'rentabilidad_ventas': "{0:.4f}".format(rentabilidad_ventas),
		'rentabilidad_inversion':"{0:.4f}".format(rentabilidad_inversion),
		'deuda_at':"{0:.4f}".format(deuda_at),
		'deuda_capital': "{0:.4f}".format(deuda_capital),
		'prueba_de_liquidez': "{0:.4f}".format(prueba_de_liquidez),
		'prueba_acida': "{0:.4f}".format(prueba_acida),
		'total_inventario':"{0:.2f}".format(total_inventario),
		'activo_corriente':"{0:.2f}".format(activo_corriente),
		'pasivo_corriente':"{0:.2f}".format(pasivo_corriente),
		'pasivo_no_corriente':"{0:.2f}".format(pasivo_no_corriente),
		'total_activo':"{0:.2f}".format(total_activo),
		'total_pasivo':"{0:.2f}".format(total_pasivo),
		'ventas':"{0:.2f}".format(ventas),
		'costo_de_venta':"{0:.2f}".format(costo_de_venta),
		'capital':"{0:.2f}".format(capital),
		'utilidad':"{0:.2f}".format(utilidad),
		'balances':balances,
		'fecha_inicio': fecha_0,
		'fecha_final': fecha_1,
	}

	return render(request, 'contabilidad_general/ratios_financieros.html', context)


def registra_nota(request):
	if request.method == 'POST':

		titulo = request.GET['titulo']
		descripcion = request.GET['descripcion']
		periodo =  Periodo.objects.last()
		id_periodo= periodo.id
		
		nota = NotaPeriodo(titulo_nota=titulo,descripcion_nota=descripcion, periodo_nota= id_periodo)
		nota.save()

		return redirect('nota_lista')
	else:
		form1 = EmpleadoForms()

	return render(request, 'contabilidad_general/.....')