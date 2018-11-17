from django.db import models
from apps.catalogo.models import Cuenta, CuentaHija
from apps.periodo.models import Periodo

# Create your models here.
class Transaccion(models.Model):
	periodo_transaccion = models.ForeignKey(Periodo, null=True, on_delete=models.CASCADE)
	fecha_transaccion = models.DateField()
	descripcion_transaccion = models.CharField(max_length=100)

	def __str__(self):
		return self.descripcion_transaccion

class Transaccion_Cuenta(models.Model):
	transaccion_tc = models.ForeignKey(Transaccion, null=True, on_delete=models.CASCADE)
	cuenta_tc = models.ForeignKey(CuentaHija, null=True, on_delete=models.CASCADE)
	debe_tc = models.FloatField()
	haber_tc = models.FloatField()

class Estado_Financiero(models.Model):
	periodo_ef = models.ForeignKey(Periodo, null=True, on_delete=models.CASCADE)
	nombre_ef = models.CharField(max_length=100)

	def __str__(self):
		return self.nombre_ef

class Estado_Financiero_Cuenta(models.Model):
	estado_financiero = models.ForeignKey(Estado_Financiero, null=True, on_delete=models.CASCADE)
	cuenta = models.ForeignKey(Cuenta, null=True, on_delete=models.CASCADE)
