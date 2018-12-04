from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from apps.catalogo.forms import CuentaForm, AgrupacionForm, HijaForm
from apps.catalogo.models import Grupo, Agrupacion, Cuenta, CuentaHija
from apps.periodo.models import BalancePeriodo, Periodo
from django.views.generic import ListView, CreateView, UpdateView
from django.http import HttpResponse 
from django.db.models import Q

# Create your views here.

def cuenta_create(request):
	form = CuentaForm()
	grupos = Grupo.objects.all()

	if request.method=='POST':
		form = CuentaForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.save()

			cuenta = Cuenta.objects.latest('id')
			agrupaciones = Cuenta.objects.filter(agrupacion=cuenta.agrupacion).order_by('codigo_cuenta')
			codigo = agrupaciones[len(agrupaciones)-2].codigo_cuenta+1

			cuenta.codigo_cuenta=codigo
			cuenta.save()

			return redirect('contabilidad_general:mostrar-cuentas')
	return render(request, 'contabilidad_general/cuenta_create.html', {'form':form, 'grupos':grupos, })
	
def load_agrupaciones(request):
	grupo_id = request.GET.get('grupo')
	agrupaciones = Agrupacion.objects.filter(codigo_grup=grupo_id).order_by('nombre_agrupacion')
	return render(request, 'contabilidad_general/dropdown_opcions.html', {'agrupaciones':agrupaciones,})

def cuenta_hija_create(request, cuenta_id):
	cuenta_p = Cuenta.objects.get(id=cuenta_id)
	cuenta_h = CuentaHija.objects.filter(padre=cuenta_id).order_by('codigo_cuenta')
	if cuenta_h:
		cod_cuenta_h=cuenta_h[len(cuenta_h)-1].codigo_cuenta+1
	else:
		cod_cuenta_h = str(cuenta_p.codigo_cuenta)+str(0)+str(1)
	cuentaid=cuenta_id

	if request.method=='POST':
		CuentaHija.objects.create(
			padre=cuenta_p,
			codigo_padre=cuenta_p.codigo_cuenta,
			nombre_cuenta=request.POST['nombre_cuenta'],
			codigo_cuenta=cod_cuenta_h,
			descripcion_cuenta=request.POST['descripcion_cuenta'],
			saldo_deudor_cuenta=0.0,
			saldo_acreedor_cuenta=0.0
			)

		return redirect('contabilidad_general:mostrar-cuentas')
	return render(request, 'contabilidad_general/cuenta_hija_create.html', {'cuenta_p':cuenta_p, 'cuenta_id': cuentaid,})

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

	for balance in balances:
		acreedor += balance.saldo_acreedor
		deudor += balance.saldo_deudor
	if acreedor==deudor:
		mensaje='Se cumple partida doble'
	else:
		mensaje='No se cumple partida doble'

	context={
		'balances':balances,
		'acreedor': acreedor,
		'deudor': deudor,
		'mensaje': mensaje,
		'fecha_inicio': fecha_0,
		'fecha_final': fecha_1,
	}

	return render(request, 'contabilidad_general/balance_comprobacion.html', context)

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

	for balance in balances:
		gastos += balance.saldo_deudor
		ingresos += balance.saldo_acreedor

	utilidad_periodo = ingresos-gastos

	context = {
		'balances': balances,
		'ingresos': round(ingresos,2),
		'gastos': round(gastos,2),
		'utilidad_periodo':round(utilidad_periodo,2),
		'fecha_inicio': fecha_0,
		'fecha_final': fecha_1,
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

	for balance in balances:
		inversiones += balance.saldo_acreedor
		desinversiones += balance.saldo_deudor

	capital_social = inversiones-desinversiones

	context = {
		'balances':balances,
		'inversiones': round(inversiones,2),
		'desinversiones': round(desinversiones,2),
		'capital_social': round(capital_social,2),
		'utilidad_periodo':utilidad_p,
		'fecha_inicio': fecha_0,
		'fecha_final': fecha_1,
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

	for balance in balances:
		haber += balance.saldo_acreedor
		debe += balance.saldo_deudor

	if debe==haber:
		mensaje='Se cumple dualidad económica'
	else:
		mensaje='No se cumple dualidad económica'

	context={
		'balances':balances,
		'debe':debe,
		'haber': haber,
		'capital_social': capital_s,
		'mensaje': mensaje,
		'fecha_final': fecha_1,
	}

	return render(request, 'contabilidad_general/balance_general.html', context)
