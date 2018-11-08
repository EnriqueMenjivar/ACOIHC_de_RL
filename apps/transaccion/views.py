from django.shortcuts import render
from apps.transaccion.forms import *
from apps.contabilidad_general.models import Periodo

# Create your views here.

def transaccion(request):

    return render(request,'transaccion/transaccion.html')