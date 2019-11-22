from django.contrib import admin
from apps.periodo.models import Periodo, BalancePeriodo,NotaPeriodo
# Register your models here.
admin.site.register(Periodo)
admin.site.register(BalancePeriodo)
admin.site.register(NotaPeriodo)
