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
	procesos_pendientes = Programacion_Proceso.objects.filter(programacion__id = id_programacion, terminado = False).order_by('id')[:1]
	materiales = CuentaHija.objects.filter(codigo_padre='1105') | CuentaHija.objects.filter(codigo_padre='1104')
	cargos = Cargo.objects.all()
	if 'btnTerminarProceso' in request.POST:
		#Se procede a saldar cuenta de proceso finalizado
		programacion_proceso = request.POST['idProgramacionProcesofrm']
		periodo = Programacion_Proceso.objects.get(id = programacion_proceso).programacion.periodo_programacion
		fecha = time.strftime("%Y-%m-%d")
		transaccion = Transaccion(fecha_transaccion = fecha, descripcion_transaccion = "Saldando cuenta de proceso finalizado", periodo_transaccion = periodo)
		transaccion.save()
		prog_proc = request.POST['idProgramacionProcesofrm']
		cuenta_proceso = Programacion_Proceso.objects.get(id = prog_proc).proceso.cuenta_proceso
		total = cuenta_proceso.debe

		if Programacion_Proceso.objects.get(id = prog_proc).proceso.id < 7:
			siguiente_proc_name = Programacion_Proceso.objects.get(id = prog_proc).proceso.proceso_siguiente
			cuenta_proceso_siguiente = Proceso.objects.get(nombre_proceso = siguiente_proc_name).cuenta_proceso
			transaccion_saldar = Transaccion_Cuenta(debe_tc = 0.00, haber_tc = total, cuenta_tc = cuenta_proceso, transaccion_tc = transaccion)
			transaccion_cargar = Transaccion_Cuenta(debe_tc = total, haber_tc = 0.00, cuenta_tc = cuenta_proceso_siguiente, transaccion_tc = transaccion)
			if transaccion_saldar.haber_tc == transaccion_cargar.debe_tc:
				transaccion_saldar.save()
				transaccion_cargar.save()

				nuevo_haber = total
				nuevo_debe = total
				CuentaHija.objects.filter(id = cuenta_proceso.id).update(debe = 0.0, haber = 0.0)
				CuentaHija.objects.filter(id = cuenta_proceso_siguiente.id).update(debe = nuevo_debe)
				Programacion_Proceso.objects.filter(id = programacion_proceso).update(terminado = True)
				prog_proc_obj = Programacion_Proceso.objects.get(id = str(int(programacion_proceso) + 1))
				asignacion_mp = Asignar_Materia_Prima(cantidad_mp = 0.00, monto = total, nombre_mp = None, proceso_prog_mp = prog_proc_obj)
				asignacion_mp.save()
				pass
			pass
		else:
			pt = Programacion_Proceso.objects.get(id = prog_proc).programacion.producto_programacion
			cuenta_inventario_pt = CuentaHija.objects.get(codigo_cuenta = pt)
			transaccion_saldar = Transaccion_Cuenta(debe_tc = 0.00, haber_tc = total, cuenta_tc = cuenta_proceso, transaccion_tc = transaccion)
			transaccion_cargar = Transaccion_Cuenta(debe_tc = total, haber_tc = 0.00, cuenta_tc = cuenta_inventario_pt, transaccion_tc = transaccion)
			if transaccion_saldar.haber_tc == transaccion_cargar.debe_tc:
				transaccion_saldar.save()
				transaccion_cargar.save()
				nuevo_haber = total
				nuevo_debe = cuenta_inventario_pt.debe + total
				CuentaHija.objects.filter(id = cuenta_proceso.id).update(debe = 0.00, haber = 0.00)
				CuentaHija.objects.filter(id = cuenta_inventario_pt.id).update(debe = nuevo_debe)
				Programacion_Proceso.objects.filter(id = programacion_proceso).update(terminado = True)
				progra = Programacion_Proceso.objects.get(id = programacion_proceso).programacion
				cantidad = float(Programacion_Proceso.objects.get(id = programacion_proceso).programacion.cantidad_programacion)
				costo_unitario = float(total)/cantidad
				Programacion.objects.filter(id = progra.id).update(estado_programacion = True, costo_unitario = costo_unitario)
				pass

		lista_programacion = Programacion.objects.all()
		return render(request,'contabilidad_costos/programacion_list.html', {'programaciones':lista_programacion})
		pass
	return render(request,'contabilidad_costos/seguimiento.html', {'procesos_pendientes':procesos_pendientes, 'materiales':materiales, 'cargos':cargos} )

def ver_detalles(request, id_programacion):
	#Se recibe el id_porgramacion para recoger todos los procesos asociados a la programacion y recorrerlos luego en el template
	programacion = Programacion.objects.get(id = id_programacion)
	producto = CuentaHija.objects.get(codigo_cuenta = programacion.producto_programacion)
	programacion_procesos = Programacion_Proceso.objects.filter(programacion = programacion)
	return render(request, 'contabilidad_costos/ver_detalles.html', {'programacion_procesos':programacion_procesos, 'producto':producto, 'programacion':programacion})

def ver_detalles_proceso(request, id_proceso):
	programacion_proceso = Programacion_Proceso.objects.get(id = id_proceso)
	programacion = programacion_proceso.programacion
	asignaciones_mp = Asignar_Materia_Prima.objects.filter(proceso_prog_mp = programacion_proceso)
	asignaciones_mo = Asignar_Mano_Obra.objects.filter(proceso_prog_mo = programacion_proceso)
	asignaciones_cif = Asignar_Cif.objects.filter(proceso_prog_cif = programacion_proceso)
	contexto = {'programacion': programacion, 'programacion_proceso': programacion_proceso, 'asignaciones_mp':asignaciones_mp, 'asignaciones_mo':asignaciones_mo, 'asignaciones_cif':asignaciones_cif}
	return render(request, 'contabilidad_costos/ver_detalles_proceso.html', contexto)

class TransaccionesProgramacion(TemplateView):

	def get(self, request, *args, **kwargs):
		if request.GET['transaccion'] == 'CargarMP':
			#Se obtendra el monto, a traves de kardex
			programacion_proceso = request.GET['programacion_proceso']
			periodo_obj = Programacion_Proceso.objects.get(id = programacion_proceso).programacion.periodo_programacion
			periodo= periodo_obj.id
			producto = request.GET['producto']
			cantidad = request.GET['cantidad']
			fecha = time.strftime("%Y-%m-%d")
			cv = list()
			costoMP = peps(periodo, fecha, producto,int(cantidad),0, True, cv)
			monto = 0.00
			for x in costoMP:
				monto = monto + x[2]
				pass
				#Aqui iva ajuste_peps()
			#Se creara la transaccion para luego cargar y abonar las cuentas correspondientes
			fecha = time.strftime("%Y-%m-%d")
			transaccion = Transaccion(fecha_transaccion = fecha, descripcion_transaccion = "Cargando materia prima al proceso productivo", periodo_transaccion = periodo_obj)
			transaccion.save()
			cuenta_mp = CuentaHija.objects.get(id = producto)
			cuenta_proceso = Programacion_Proceso.objects.get(id = programacion_proceso).proceso.cuenta_proceso
			transaccion_mp = Transaccion_Cuenta(debe_tc = 0.00, haber_tc = monto, cuenta_tc = cuenta_mp, transaccion_tc = transaccion)
			transaccion_proceso = Transaccion_Cuenta(debe_tc = monto, haber_tc = 0.00, cuenta_tc = cuenta_proceso, transaccion_tc = transaccion)
			
			#Se comprobara partida doble y luego aplicar cambios en cuentas hijas
			if transaccion_mp.haber_tc == transaccion_proceso.debe_tc:
				transaccion_mp.save()
				transaccion_proceso.save()
				nuevo_haber = cuenta_mp.haber + monto
				nuevo_debe = cuenta_proceso.debe + monto
				CuentaHija.objects.filter(id = cuenta_mp.id).update(haber = nuevo_haber)
				CuentaHija.objects.filter(id = cuenta_proceso.id).update(debe = nuevo_debe)
				prog_proc_obj = Programacion_Proceso.objects.get(id = programacion_proceso) 
				asignacion_mp = Asignar_Materia_Prima(cantidad_mp = float(cantidad), monto = monto, nombre_mp = cuenta_mp, proceso_prog_mp = prog_proc_obj)
				asignacion_mp.save()
				#Se alistara JSON para reflejar datos en la tabla de mp
				data = serializers.serialize('json',[asignacion_mp],fields = ('proceso_prog_mp','nombre_mp','cantidad_mp','monto'))
				return HttpResponse(data, content_type = 'application/json')
				pass


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
			#Se procedera a calcular los montos de mod, mp y cp
			prog_proc_obj = Programacion_Proceso.objects.get(id = programacion_proceso)
			asignaciones_mp = Asignar_Materia_Prima.objects.filter(proceso_prog_mp = prog_proc_obj)
			asignaciones_mod = Asignar_Mano_Obra.objects.filter(proceso_prog_mo = prog_proc_obj)

			monto_mp = 0.00
			monto_mod = 0.00
			for x in asignaciones_mp:
				monto_mp = monto_mp + x.monto
				pass
			for x in asignaciones_mod:
				monto_mod = monto_mod + x.monto
				pass
			monto_cp = monto_mp + monto_mod
			total_cif = 0.00

			#Se calculara los CIF
			if baseAsignacion == 'mod':
				total_cif = monto_mod*float(porcentajeAsignacion)
				pass

			elif baseAsignacion == 'mp':
				total_cif = monto_mp*float(porcentajeAsignacion)
				pass

			elif baseAsignacion == 'cp':
				total_cif = monto_cp*float(porcentajeAsignacion)
				pass

			#Se procedera a realizar las transacciones
			fecha = time.strftime("%Y-%m-%d")
			periodo = Programacion_Proceso.objects.get(id = programacion_proceso).programacion.periodo_programacion
			transaccion = Transaccion(fecha_transaccion = fecha, descripcion_transaccion = "Cargando CIF a proceso", periodo_transaccion = periodo)
			transaccion.save()

			cuenta_variacion = CuentaHija.objects.get(codigo_cuenta = 610101)
			cuenta_proceso = Programacion_Proceso.objects.get(id = programacion_proceso).proceso.cuenta_proceso

			transaccion_proceso = Transaccion_Cuenta(debe_tc = total_cif, haber_tc = 0.00, cuenta_tc = cuenta_proceso, transaccion_tc = transaccion)
			transaccion_variacion = Transaccion_Cuenta(debe_tc = 0.00, haber_tc = total_cif, cuenta_tc = cuenta_variacion, transaccion_tc = transaccion)

			#Se procede a comprobar partida doble y cerrar transacciones

			if transaccion_proceso.debe_tc == transaccion_variacion.haber_tc:
				transaccion_proceso.save()
				transaccion_variacion.save()
				nuevo_haber = cuenta_variacion.haber + total_cif
				nuevo_debe = cuenta_proceso.debe + total_cif
				CuentaHija.objects.filter(id = cuenta_variacion.id).update(haber = nuevo_haber)
				CuentaHija.objects.filter(id = cuenta_proceso.id).update(debe = nuevo_debe)
				prog_proc = Programacion_Proceso.objects.get(id = programacion_proceso)
				asignacion_cif = Asignar_Cif(base_cif = baseAsignacion, porcentaje_cif = float(porcentajeAsignacion), proceso_prog_cif = prog_proc, monto = total_cif)
				asignacion_cif.save()
				data = serializers.serialize('json',[asignacion_cif],fields = ('base_cif','porcentaje_cif','proceso_prog_cif','monto'))
				return HttpResponse(data, content_type = 'application/json')
				pass
			pass

		data = serializers.serialize('json',[])
		return HttpResponse(data, content_type = 'application/json')

class Lista_Empleados(ListView):
	model = Empleado
	template_name = 'contabilidad_costos/empleado_list'


class planilla_general(ListView):
	model = Planilla
	template_name = 'contabilidad_costos/planillaGeneral.html'


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
			v = (salario_Mensual*0.5/12)*(1.3) + (salario_Mensual*0.5/12)*(0.075 + 0.065);
			vacaciones = round(v,2);
			a = (salario_Mensual*19/(12*30));
			aguinaldo = round(a,2);
			salario_total = salario_Mensual + iss + afp + insaforp + vacaciones+ aguinaldo;
	

			
			planilla = Planilla(periodo_planilla= periodo, empleado_planilla= empleado, isss_planilla=iss, afp_planilla= afp, vacacion_planilla=vacaciones, aguinaldo_planilla=aguinaldo, insaforp=insaforp, salario_total=salario_total)
			planilla.save()

		return redirect('empleado_lista')
	else:
		form1 = EmpleadoForms()

	return render(request, 'contabilidad_costos/empleado_registrar.html',{'form1': form1 })


def lista_Empleados(request):
	empleados = Empleado.objects.all()
	planillas = Planillas.objects.all()
	return render(request,'contabilidad_costos/programacion_list.html', {'empleados':empleados, 'planillas':planillas})

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
