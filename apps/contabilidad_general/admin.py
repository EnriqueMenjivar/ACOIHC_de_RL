from django.contrib import admin
from apps.contabilidad_general.models import Transaccion, Transaccion_Cuenta, Estado_Financiero, Estado_Financiero_Cuenta 
# Register your models here.
# -*- coding: utf-8 -*-
admin.site.register(Transaccion)
admin.site.register(Transaccion_Cuenta)
admin.site.register(Estado_Financiero)
admin.site.register(Estado_Financiero_Cuenta)