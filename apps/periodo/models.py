from django.db import models
from apps.catalogo.models import Cuenta, CuentaHija

# Create your models here.
class Periodo(models.Model):
	inicio_periodo = models.DateField()
	final_periodo = models.DateField()
	estado_periodo = models.BooleanField(default=False)
	periodo_ajuste = models.BooleanField(default=False)
		
class BalancePeriodo(models.Model):
	hija_balance = models.ForeignKey(CuentaHija, null=True, on_delete=models.CASCADE)
	periodo_balance = models.ForeignKey(Periodo, null=True, on_delete=models.CASCADE)
	cuenta_balance = models.ForeignKey(Cuenta, null=True, on_delete=models.CASCADE)
	saldo_deudor = models.FloatField(default=0.0)
	saldo_acreedor = models.FloatField(default=0.0)
	saldo_deudor_h = models.FloatField(default=0.0)
	saldo_acreedor_h = models.FloatField(default=0.0)
