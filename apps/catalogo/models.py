from django.db import models


# Create your models here.
class Grupo(models.Model):
	nombre_grupo = models.CharField(max_length=100)
	codigo_grupo = models.CharField(max_length=2)
	def __str__(self):
		return self.nombre_grupo


class Agrupacion(models.Model):
	codigo_grup = models.ForeignKey(Grupo, null=True, on_delete=models.CASCADE)
	nombre_agrupacion = models.CharField(max_length=100)
	codigo_agrupacion = models.CharField(max_length=3)
	def __str__(self):
		return self.nombre_agrupacion

class Cuenta(models.Model):
	codigo_agrup = models.ForeignKey(Agrupacion, null=True, on_delete=models.CASCADE)
	codigo_padre = models.CharField(max_length=4)
	nombre_cuenta = models.CharField(max_length=100)
	codigo_cuenta = models.CharField(max_length=5)
	descripcion_cuenta = models.CharField(max_length=100)
	saldo_deudor_cuenta = models.FloatField()
	saldo_acreedor_cuenta = models.FloatField()

	def __str__(self):
		return self.nombre_cuenta



