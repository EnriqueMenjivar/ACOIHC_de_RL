from django.db import models
from apps.catalogo.models import Cuenta
from apps.contabilidad_general.models import Transaccion_Cuenta
from apps.periodo.models import Periodo
# Create your models here.

class Kardex(models.Model):
	cuenta_kardex = models.ForeignKey(Cuenta, null=True, on_delete=models.CASCADE)
	cantidad_existencia = models.IntegerField()
	precio_unitario_peps = models.FloatField()

class Entrada_Salida(models.Model):
	transaccion = models.ForeignKey(Transaccion_Cuenta, null=True, on_delete=models.CASCADE)
	kardex = models.ForeignKey(Kardex, null=True, on_delete=models.CASCADE)
	cantidad_unidades = models.IntegerField()
	precio_unitario = models.FloatField()

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

class Programacion(models.Model):
	periodo_programacion = models.ForeignKey(Periodo, null=True, on_delete=models.CASCADE)
	fecha_programacion = models.DateField()
	producto_programacion = models.CharField(max_length=100)
	cantidad_programacion = models.IntegerField()
	estado_programacion = models.BooleanField(default= False)
	def __str__(self):
		return self.producto_programacion

class Proceso(models.Model):
	programacion = models.ForeignKey(Programacion, null=True, on_delete=models.CASCADE)
	proceso_siguiente = models.CharField(max_length=100)
	nombre_proceso = models.CharField(max_length=100)


	def __str__(self):
		return self.nombre_proceso

class Asignar_Materia_Prima(models.Model):
	proceso_mp = models.ForeignKey(Proceso, null=True, on_delete=models.CASCADE)
	nombre_mp = models.CharField(max_length=100)
	cantidad_mp = models.FloatField()
	precio_unitario_mp = models.FloatField()

	def __str__(self):
		return self.nombre_mp

class Asignar_Cif(models.Model):
	proceso_cif = models.ForeignKey(Proceso, null=True, on_delete=models.CASCADE)
	base_cif = models.CharField(max_length=100)
	porcentaje_cif = models.FloatField()

class Asignar_Mano_Obra(models.Model):
	proceso_mo = models.ForeignKey(Proceso, null=True, on_delete=models.CASCADE)
	cargo_mo = models.ForeignKey(Cargo, null=True, on_delete=models.CASCADE)
	cantidad_horas_empleado = models.FloatField()
	cantidad_empleados = models.IntegerField()


