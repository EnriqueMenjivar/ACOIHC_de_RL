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
	cod_cuenta=str(Cuenta.objects.latest('id').codigo_cuenta)
	cod_cuenta=cod_cuenta[2:len(cod_cuenta)]
	cod_correlativo = str(int(cod_cuenta)+1)
	#cod_correlativo = str(cod_cuenta+1)

	if request.method=='POST':
		form = CuentaForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.save()

			cuenta = Cuenta.objects.latest('id')
			cod_cuenta =cuenta.agrupacion.codigo_agrupacion
			cuenta.codigo_cuenta = int(cod_cuenta+cod_correlativo)
			cuenta.save()

			return redirect('contabilidad_general:mostrar-cuentas')
	return render(request, 'contabilidad_general/cuenta_create.html', {'form':form, 'grupos':grupos, })
	
def load_agrupaciones(request):
	grupo_id = request.GET.get('grupo')
	agrupaciones = Agrupacion.objects.filter(codigo_grup=grupo_id).order_by('nombre_agrupacion')
	return render(request, 'contabilidad_general/dropdown_opcions.html', {'agrupaciones':agrupaciones,})

def cuenta_hija_create(request, cuenta_id):
	cuenta_p = Cuenta.objects.get(id=cuenta_id)
	cuenta_h = CuentaHija.objects.filter(padre=cuenta_id)
	if cuenta_h:
		cod_cuenta_h=cuenta_h[len(cuenta_h)-1].codigo_cuenta+1
	else:
		cod_cuenta_h = str(cuenta_p.codigo_cuenta)+str(1)
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
	cuentas = Cuenta.objects.all()
	return render(request, 'contabilidad_general/catalogo_show.html', {'cuentas':cuentas})

def hijas_show(request, cuenta_id):
	hijas = CuentaHija.objects.filter(padre=cuenta_id)
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
		'grupos':grupos,
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
'''
def sumar(request):
	cuenta_h=CuentaHija.objects.all()
	cuenta_p=Cuenta.objects.all()
	if 'btnCerrarPeriodo' in request.POST:
		for hija in cuenta_h:
			saldo=hija.debe-hija.haber
			if saldo>0:
				hija.saldo_deudor_cuenta=saldo
				hija.save()
			else:
				hija.saldo_acreedor_cuenta=abs(saldo)
				hija.save()
	return render(request, 'contabilidad_general/prueba.html', {'cuenta_p':cuenta_p})
'''

def cerrar_periodo(request, periodo_id):
	if 'btnCerrarPeriodo' in request.POST:
		cuenta = Cuenta.objects.all()
		hija = CuentaHija.objects.all()
		periodo = Periodo.objects.get(id=periodo_id)
		
		i=0
		while i<len(cuenta):
			bp=BalancePeriodo()
			if i<len(hija):
				bp.hija_balance=hija[i]
				bp.saldo_deudor_h=hija[i].saldo_deudor_cuenta
				bp.saldo_acreedor_h=hija[i].saldo_acreedor_cuenta
			bp.periodo_balance=periodo
			bp.cuenta_balance=cuenta[i]
			bp.saldo_deudor=cuenta[i].saldo_deudor_cuenta
			bp.saldo_acreedor=cuenta[i].saldo_acreedor_cuenta
			bp.save()
			i+=1
	return render(request, 'contabilidad_general/prueba.html', {'periodo_id':periodo_id})

def sumar(request):
	i=0
	j=0
	cuenta_p=''
	if 'btnCerrarPeriodo' in request.POST:
		cuenta_p = Cuenta.objects.all()
		cuenta_h = CuentaHija.objects.all()

		while i<len(cuenta_p):
			while j<len(cuenta_h):
				if cuenta_p[i].codigo_cuenta==cuenta_h[j].codigo_padre:
					cuenta_p[i].saldo_deudor_cuenta += cuenta_h[j].saldo_deudor_cuenta
					cuenta_p[i].saldo_acreedor_cuenta += cuenta_h[j].saldo_acreedor_cuenta
					cuenta_p[i].save()
				j+=1
			i+=1
	return render(request, 'contabilidad_general/prueba.html', {'cuenta_p':cuenta_p})

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
	#balances =BalancePeriodo.objects.filter(periodo_balance=periodo_id, cuenta_balance__agrupacion=41|51 )
	balances = BalancePeriodo.objects.filter(Q(periodo_balance=periodo_id), 
											Q(cuenta_balance__agrupacion__codigo_agrupacion=41)|
											Q(cuenta_balance__agrupacion__codigo_agrupacion=51)).\
											order_by('cuenta_balance__nombre_cuenta')
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
											Q(cuenta_balance__agrupacion__codigo_agrupacion=51))
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
		mensaje='Se cumple partida doble'
	else:
		mensaje='No se cumple partida doble'

	context={
		'balances':balances,
		'debe':debe,
		'haber': haber,
		'capital_social': capital_s,
		'mensaje': mensaje,
		'fecha_final': fecha_1,
	}

	return render(request, 'contabilidad_general/balance_general.html', context)

'''#Consulta de prueba
	cuenta = Cuenta.objects.latest('id')
	cod_agrupacion = cuenta.agrupacion.codigo_agrupacion
	vector_correlativo = Cuenta.objects.filter(codigo_cuenta__startswith=cod_agrupacion).order_by('codigo_cuenta')
	codigo_ultima_cuenta = vector_correlativo[len(vector_correlativo)-1].codigo_cuenta
	cod_correlativo = codigo_ultima_cuenta[2:len(codigo_ultima_cuenta)]
	cod_correlativo = str(int(cod_correlativo)+1)
	cuenta.codigo_cuenta = cod_cuenta+cod_correlativo
	cuenta.save()
'''