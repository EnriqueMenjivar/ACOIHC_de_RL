from django.db import models
from apps.catalogo.models import Cuenta, CuentaHija
from apps.contabilidad_general.models import Transaccion_Cuenta
from apps.periodo.models import Periodo
# Create your models here.

class Kardex(models.Model):
	cuenta_kardex = models.ForeignKey(CuentaHija, null=True, on_delete=models.CASCADE)
	cantidad_existencia = models.IntegerField()
	precio_unitario_peps = models.FloatField()

class Entrada_Salida(models.Model):
	periodo_es = models.ForeignKey(Periodo, null=True, on_delete=models.CASCADE)
	fecha_es = models.DateField()
	kardex = models.ForeignKey(Kardex, null=True, on_delete=models.CASCADE)
	cantidad_unidades = models.IntegerField()
	precio_unitario = models.FloatField()
	tipo_movimiento = models.BooleanField(default=False)
	cabeza_kardex = models.BooleanField(default=False)
	cola_kardex = models.BooleanField(default=False)
	siguiente_kardex = models.CharField(max_length=5, blank=True, null=True)

class Entrada_Salida_Respaldo(models.Model):
	periodo_esr = models.ForeignKey(Periodo, null=True, on_delete=models.CASCADE)
	fecha_esr = models.DateField()
	kardexr = models.ForeignKey(Kardex, null=True, on_delete=models.CASCADE)
	cantidad_unidadesr = models.IntegerField()
	precio_unitarior = models.FloatField()
	tipo_movimientor = models.BooleanField(default=False)


class Cargo(models.Model):
	nombre_cargo = models.CharField(max_length=100)
	sueldo_base = models.FloatField()

	def __str__(self):
		return self.nombre_cargo

class Empleado(models.Model):
	cargo_empleado = models.ForeignKey(Cargo, null=True, on_delete=models.CASCADE)
	nombre_empleado = models.CharField(max_length=100)
	apellido_empleado = models.CharField(max_length=100)
	dui_empleado = models.CharField(max_length=100)
	Nisss_empleado = models.CharField(max_length=100)
	Nafp_empleado = models.CharField(max_length=100)
	años_empleado = models.FloatField()

	def __str__(self):
		return self.nombre_empleado

class Planilla(models.Model):
	periodo_planilla = models.ForeignKey(Periodo, null=True, on_delete=models.CASCADE)
	empleado_planilla = models.ForeignKey(Empleado, null=True, on_delete=models.CASCADE)
	isss_planilla = models.FloatField()
	afp_planilla = models.FloatField()
	vacacion_planilla = models.FloatField()
	aguinaldo_planilla = models.FloatField()
	insaforp = models.FloatField()
	salario_total = models.FloatField()

class Programacion(models.Model):
	periodo_programacion = models.ForeignKey(Periodo, null=True, on_delete=models.CASCADE)
	fecha_programacion = models.DateField()
	producto_programacion = models.CharField(max_length=100)
	cantidad_programacion = models.IntegerField()
	estado_programacion = models.BooleanField(default= False)
	costo_unitario = models.FloatField(default=0.00)
	def __str__(self):
		return self.producto_programacion


class Proceso(models.Model):
	nombre_proceso = models.CharField(max_length=100)
	proceso_siguiente = models.CharField(max_length=100)
	cuenta_proceso = models.ForeignKey(CuentaHija, null=True, on_delete=models.CASCADE)
	def __str__(self):
		return self.nombre_proceso

class Programacion_Proceso(models.Model):
	programacion = models.ForeignKey(Programacion, null=True, on_delete=models.CASCADE)
	proceso = models.ForeignKey(Proceso, null=True, on_delete=models.CASCADE)
	terminado = models.BooleanField(default= False)


class Asignar_Materia_Prima(models.Model):
	proceso_prog_mp = models.ForeignKey(Programacion_Proceso, null=True, on_delete=models.CASCADE)
	#nombre_mp = models.CharField(max_length=100)
	nombre_mp = models.ForeignKey(CuentaHija, null=True, on_delete=models.CASCADE)
	cantidad_mp = models.FloatField()
	monto = models.FloatField()


class Asignar_Cif(models.Model):
	proceso_prog_cif = models.ForeignKey(Programacion_Proceso, null=True, on_delete=models.CASCADE)
	base_cif = models.CharField(max_length=100)
	porcentaje_cif = models.FloatField()
	monto = models.FloatField()

class Asignar_Mano_Obra(models.Model):
	proceso_prog_mo = models.ForeignKey(Programacion_Proceso, null=True, on_delete=models.CASCADE)
	cargo_mo = models.ForeignKey(Cargo, null=True, on_delete=models.CASCADE)
	cantidad_horas_empleado = models.FloatField()
	cantidad_empleados = models.IntegerField()
	monto = models.FloatField()


