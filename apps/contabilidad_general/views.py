from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from apps.catalogo.forms import CuentaForm, AgrupacionForm, HijaForm
from apps.catalogo.models import Grupo, Agrupacion, Cuenta, CuentaHija
from apps.periodo.models import BalancePeriodo, Periodo
from django.views.generic import ListView, CreateView, UpdateView

# Create your views here.

class CuentaCreateView(CreateView):
	model = Cuenta
	form_class = CuentaForm
	template_name = 'contabilidad_general/cuenta_create.html'
	success_url =reverse_lazy('home')


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

			return redirect('home')
	return render(request, 'contabilidad_general/cuenta_create.html', {'form':form, 'grupos':grupos, })
	
def load_agrupaciones(request):
	grupo_id = request.GET.get('grupo')
	agrupaciones = Agrupacion.objects.filter(codigo_grup=grupo_id).order_by('nombre_agrupacion')
	return render(request, 'contabilidad_general/dropdown_opcions.html', {'agrupaciones':agrupaciones,})

def cuenta_hija_create(request, cuenta_id):
	cuenta_p = Cuenta.objects.get(id=cuenta_id)
	cod_cuenta_h = str(cuenta_p.codigo_cuenta)+str(1)
	cuentaid=cuenta_id

	if request.method=='POST':
		CuentaHija.objects.create(
			padre=cuenta_id,
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

def cerrar_periodo(request, periodo_id):
	if 'btnCerrarPeriodo' in request.POST:
		cuenta = Cuenta.objects.all()
		periodo = Periodo.objects.get(id=periodo_id)
		
		i=0
		while i<len(cuenta):
			bp=BalancePeriodo()
			bp.periodo_balance=periodo
			bp.cuenta_balance=cuenta[i]
			bp.saldo_deudor=cuenta[i].saldo_deudor_cuenta
			bp.saldo_acreedor=cuenta[i].saldo_acreedor_cuenta
			bp.save()
			i+=1
	return render(request, 'contabilidad_general/prueba.html', {'periodo_id':periodo_id})

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