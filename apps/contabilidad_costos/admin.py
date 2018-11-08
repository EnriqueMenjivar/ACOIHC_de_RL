from django.contrib import admin
from apps.contabilidad_costos.models import Kardex, Entrada_Salida, Cargo, Empleado, Planilla, Programacion, Proceso, Asignar_Materia_Prima, Asignar_Cif, Asignar_Mano_Obra
# Register your models here.
admin.site.register(Kardex)
admin.site.register(Entrada_Salida)
admin.site.register(Cargo)
admin.site.register(Empleado)
admin.site.register(Planilla)
admin.site.register(Programacion)
admin.site.register(Proceso)
admin.site.register(Asignar_Materia_Prima)
admin.site.register(Asignar_Cif)
admin.site.register(Asignar_Mano_Obra)