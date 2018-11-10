from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from apps.catalogo.forms import CuentaForm, AgrupacionForm
from apps.catalogo.models import Grupo, Agrupacion, Cuenta
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
	cod_cuenta=Cuenta.objects.latest('id').codigo_cuenta
	cod_cuenta=cod_cuenta[2:len(cod_cuenta)]
	cod_correlativo = str(int(cod_cuenta)+1)

	if request.method=='POST':
		form = CuentaForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.save()

			cuenta = Cuenta.objects.latest('id')
			cod_cuenta =cuenta.agrupacion.codigo_agrupacion
			cuenta.codigo_cuenta = cod_cuenta+cod_correlativo
			cuenta.save()

			return redirect('home')
	return render(request, 'contabilidad_general/cuenta_create.html', {'form':form, 'grupos':grupos, })
	
def load_agrupaciones(request):
	grupo_id = request.GET.get('grupo')
	agrupaciones = Agrupacion.objects.filter(codigo_grup=grupo_id).order_by('nombre_agrupacion')
	return render(request, 'contabilidad_general/dropdown_opcions.html', {'agrupaciones':agrupaciones,})

def cuenta_hija_create(request, cuenta_id):
	cuenta_p = Cuenta.objects.get(id=cuenta_id)
	cod_cuenta_h = cuenta_p.codigo_cuenta+str(1)
	cuentaid=cuenta_id

	if request.method=='POST':
		Cuenta.objects.create(
			agrupacion=cuenta_p.agrupacion,
			codigo_padre=cuenta_p.codigo_cuenta,
			nombre_cuenta=request.POST['nombre_cuenta'],
			codigo_cuenta=cod_cuenta_h,
			descripcion_cuenta=request.POST['descripcion_cuenta'],
			saldo_deudor_cuenta=0.0,
			saldo_acreedor_cuenta=0.0
			)
		return redirect('home')
	return render(request, 'contabilidad_general/cuenta_hija_create.html', {'cuenta_p':cuenta_p, 'cuenta_id': cuentaid,})

			
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