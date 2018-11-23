from django.shortcuts import render, HttpResponse, redirect
from apps.contabilidad_costos.models import *
from apps.periodo.models import *
from apps.catalogo.models import *
from apps.contabilidad_general.models import *
from apps.contabilidad_costos.forms import EmpleadoForms
from apps.contabilidad_costos.peps import *
from django.views.generic import TemplateView, ListView, CreateView
from django.urls import reverse_lazy
from datetime import datetime
from django.core import serializers
import datetime, time
from decimal import Decimal


def programacion_list(request):
	lista_programacion = Programacion.objects.all()
	return render(request,'contabilidad_costos/programacion_list.html', {'programaciones':lista_programacion})

def programacion_nueva(request):
	periodos = Periodo.objects.all()
	productos = CuentaHija.objects.filter(codigo_padre='1103')
	contexto = {'periodos':periodos, 'productos':productos}

	if 'btnGuardarProgra' in request.POST:
		periodo = Periodo.objects.get(id = request.POST['periodoSeleccionado'])
		fecha = request.POST['fecha']
		producto = request.POST['producto']
		cantidad = request.POST['cantidad']
		programaciones = Programacion.objects.all().order_by('id')

		if len(programaciones) == 0:
			id_programacion = 1
		else:	
			id_programacion =programaciones[len(programaciones) - 1].id + 1

		programacion_nueva = Programacion(id =id_programacion, fecha_programacion = fecha, producto_programacion = producto, cantidad_programacion = cantidad, estado_programacion = False, periodo_programacion = periodo)
		programacion_nueva.save()

		for x in [1,2,3,4,5,6,7]:
			programaciones_procesos = Programacion_Proceso.objects.all().order_by('id')
			if len(programaciones_procesos) == 0:
				id_programacion_proceso = 1
			else:
				id_programacion_proceso = programaciones_procesos[len(programaciones_procesos) - 1].id + 1

			programacion_proceso = Programacion_Proceso(id = id_programacion_proceso, programacion = programacion_nueva, proceso = Proceso.objects.get(id = x), terminado = False)
			programacion_proceso.save()
			pass
		return redirect('/contabilidad_costos/programaciones_lista/')

	return render(request, 'contabilidad_costos/programacion_nueva.html', contexto)


def seguimiento(request, id_programacion):
	procesos_pendientes = Programacion_Proceso.objects.filter(programacion__id = id_programacion, terminado = False)[:1]
	materiales = CuentaHija.objects.filter(codigo_padre='1105') | CuentaHija.objects.filter(codigo_padre='1104')
	cargos = Cargo.objects.all()
	return render(request,'contabilidad_costos/seguimiento.html', {'procesos_pendientes':procesos_pendientes, 'materiales':materiales, 'cargos':cargos} )

"""class ProgramacionesAjaxView(TemplateView):

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
		return HttpResponse(data, content_type = 'application/json')"""

class TransaccionesProgramacion(TemplateView):

	def get(self, request, *args, **kwargs):
		if request.GET['transaccion'] == 'CargarMP':
			programacion_proceso = request.GET['programacion_proceso']
			periodo = Programacion_Proceso.objects.get(id = programacion_proceso).programacion.periodo_programacion.id
			producto = request.GET['producto']
			cantidad = request.GET['cantidad']
			fecha = time.strftime("%Y-%m-%d")
			costoMP = peps(periodo, fecha, producto,cantidad,0, True, 0)
			print(costoMP)
			pass

		elif request.GET['transaccion'] == 'CargarMOD':
			programacion_proceso = request.GET['programacion_proceso']
			periodo = Programacion_Proceso.objects.get(id = programacion_proceso).programacion.periodo_programacion
			cargoSueldo = request.GET['cargo']
			cargo = cargoSueldo.split("/")[0]
			sueldo = Decimal((cargoSueldo.split("/")[1]+"0").replace(",","."))
			cantidadEmpleados = int(request.GET['cantidadEmpleados'])
			cantidadHRSempleado = int(request.GET['cantidadHRSempleado'])
			monto = float(sueldo*cantidadEmpleados*cantidadHRSempleado)
			fecha = time.strftime("%Y-%m-%d")
			transaccion = Transaccion(fecha_transaccion = fecha, descripcion_transaccion = "Cargando mano de obra a proceso", periodo_transaccion = periodo)
			transaccion.save()
			cuenta_sueldo = CuentaHija.objects.get(codigo_cuenta = 410101)
			codigo_cuenta = Programacion_Proceso.objects.get(id = programacion_proceso).proceso.cuenta_proceso.codigo_cuenta
			cuenta_proceso = CuentaHija.objects.get(codigo_cuenta = codigo_cuenta)
			transaccion_sueldo = Transaccion_Cuenta(debe_tc = 0.00, haber_tc = monto, cuenta_tc = cuenta_sueldo, transaccion_tc = transaccion)
			transaccion_proceso = Transaccion_Cuenta(debe_tc = monto, haber_tc = 0.00, cuenta_tc = cuenta_proceso, transaccion_tc = transaccion)
			
			if transaccion_proceso.debe_tc == transaccion_sueldo.haber_tc:
				transaccion_sueldo.save()
				transaccion_proceso.save()
				nuevo_haber = cuenta_sueldo.haber + monto
				nuevo_debe = cuenta_proceso.debe + monto
				CuentaHija.objects.filter(id = cuenta_sueldo.id).update(haber = nuevo_haber)
				CuentaHija.objects.filter(id = cuenta_proceso.id).update(debe = nuevo_debe)
				prog_proc = Programacion_Proceso.objects.get(id = programacion_proceso)
				cargo_obj = Cargo.objects.get(id = cargo)
				asignacion_mo = Asignar_Mano_Obra(cantidad_horas_empleado = float(cantidadHRSempleado), cantidad_empleados = cantidadEmpleados, cargo_mo = cargo_obj, proceso_prog_mo = prog_proc, monto = monto)
				asignacion_mo.save()
				data = serializers.serialize('json',[asignacion_mo],fields = ('cantidad_horas_empleado','cantidad_empleados','cargo_mo','proceso_prog_mo', 'monto'))
				return HttpResponse(data, content_type = 'application/json')
			pass

		elif request.GET['transaccion'] == 'CargarCIF':
			programacion_proceso = request.GET['programacion_proceso']
			baseAsignacion = request.GET['baseAsignacion']
			porcentajeAsignacion = request.GET['porcentajeAsignacion']
			pass

		data = serializers.serialize('json',[])
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