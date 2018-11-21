from django.shortcuts import render, HttpResponse, redirect
from apps.contabilidad_costos.models import *
from apps.periodo.models import *
from apps.catalogo.models import *
from apps.contabilidad_costos.forms import EmpleadoForms
from django.views.generic import TemplateView, ListView, CreateView
from django.urls import reverse_lazy
from datetime import datetime
from django.core import serializers

def programacion_list(request):
	lista_programacion = Programacion.objects.all()
	return render(request,'contabilidad_costos/programacion_list.html', {'programaciones':lista_programacion})

def programacion_nueva(request):
	periodos = Periodo.objects.all()
	productos = Cuenta.objects.filter(codigo_padre='1141')
	materiales = Cuenta.objects.filter(codigo_padre='1143')
	cargos = Cargo.objects.all()
	contexto = {'periodos':periodos, 'productos':productos, 'materiales':materiales, 'cargos':cargos}
	return render(request, 'contabilidad_costos/programacion_nueva.html', contexto)

class ProgramacionesAjaxView(TemplateView):

	def get(self, request, *args, **kwargs):
		periodo = request.GET['periodo']
		periodoObject = Periodo.objects.get(id = periodo)
		fecha = request.GET['fecha']
		producto = request.GET['producto']
		productoNombre = Cuenta.objects.get(codigo_cuenta = producto).nombre_cuenta
		cantidad = request.GET['cantidad']
		programaciones = Programacion.objects.all().order_by('id')
		id_programacion =programaciones[len(programaciones) - 1].id + 1
		programacion = Programacion(id=id_programacion, periodo_programacion = periodoObject, fecha_programacion = fecha, producto_programacion = productoNombre, cantidad_programacion= int(cantidad))
		programacion.save()
		programacion_list = [programacion]
		data = serializers.serialize('json',programacion_list,fields = ('id'))
		return HttpResponse(data, content_type = 'application/json')
		

class Lista_Empleados(ListView):
	model = Empleado
	template_name = 'contabilidad_costos/empleado_list'


def planilla_general(request):
	return render(request,'contabilidad_costos/planillaGeneral.html')


def planilla_empleado(request, id_empleado):
	empleado = Empleado.objects.get(id = id_empleado)
	planilla = Planilla.objects.get(id = id_empleado)

	return render(request, 'contabilidad_costos/planillaEmpleado.html', {'empleado':empleado, 'planilla':planilla} )



def registra_Empleado(request):
	if request.method == 'POST':
		form1 = EmpleadoForms(request.POST)
		if form1.is_valid():

			form1.save()
			
			periodo = Periodo.objects.get(id=1)
			empleado = Empleado.objects.last()
			salario_Mensual = empleado.cargo_empleado.sueldo_base
			iss = salario_Mensual*0.075;
			afp = salario_Mensual*0.065;
			insaforp = salario_Mensual*0.01;
			vacaciones = 0;
			aguinaldo = 0;
			salario_total = salario_Mensual + iss + afp + insaforp ;
	

			
			planilla = Planilla(periodo_planilla= periodo, empleado_planilla= empleado, isss_planilla=iss, afp_planilla= afp, vacacion_planilla=vacaciones, aguinaldo_planilla=aguinaldo, insaforp=insaforp, salario_total=salario_total)
			planilla.save()

		return redirect('empleado_lista')
	else:
		form1 = EmpleadoForms()

	return render(request, 'contabilidad_costos/empleado_registrar.html',{'form1': form1 })

def lista_kardex(request):
	lista_kardex = list() # creamos la lista que enviaremos al contexto
	list_interna = list() # me permitira guardar en la primera posicion el kardex, y en la segunda posicion una lista de precio_un y cant
	kardexs = Kardex.objects.all() #traemos todos los kardex
	for kardex in kardexs:
		list_interna.append(kardex)
		es_existe = Entrada_Salida.objects.filter(kardex= kardex).exists()
		if es_existe:
			es = Entrada_Salida.objects.filter(kardex=kardex, cantidad_unidades__gt = 0 )
			list_interna.append(es)
		lista_kardex.append(list_interna)
		list_interna = []
	contexto={
	'lista_kardex':lista_kardex
	}
	return render(request,'contabilidad_costos/lista_kardex.html',contexto)

def kardex(request,id):
	kardex_existe = Kardex.objects.filter(id = id).exists #vemos si el kardex existe
	if kardex_existe:
		kardex = Kardex.objects.get(id = id)
		periodo_actual = Periodo.objects.get(estado_periodo =False)
		esr = Entrada_Salida_Respaldo.objects.filter(kardexr=kardex,periodo_esr=periodo_actual)
		es = Entrada_Salida.objects.filter(kardex=kardex, cantidad_unidades__gt = 0 )
	contexto={
	'kardex':kardex,
	'esr':esr,
	'es':es
	}
	return render(request,'contabilidad_costos/kardex.html',contexto)