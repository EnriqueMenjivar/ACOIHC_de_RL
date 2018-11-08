from django.db import models
from apps.catalogo.models import Cuenta

# Create your models here.
class Periodo(models.Model):
	inicio_periodo = models.DateField()
	final_periodo = models.DateField()
	estado_periodo = models.BooleanField(default=False)

	def __str__(self):
		return self.estado_periodo
		
class BalancePeriodo(models.Model):
	periodo_balance = models.ForeignKey(Periodo, null=True, on_delete=models.CASCADE)
	cuenta_balance = models.ForeignKey(Cuenta, null=True, on_delete=models.CASCADE)
	saldo_deudor = models.FloatField()
	saldo_acreedor = models.FloatField()
