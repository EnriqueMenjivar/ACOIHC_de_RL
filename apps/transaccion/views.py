from django.shortcuts import render
from apps.transaccion.forms import TransaccionForm, Transaccion_CuentaForm
from apps.periodo.models import Periodo
from apps.catalogo.models import Cuenta
from django.http import JsonResponse

# Create your views here.


def transaccion(request):
    cuentas = Cuenta.objects.all()
    periodo = Periodo.objects.get(estado_periodo=False)

    form1 = TransaccionForm()
    form2=Transaccion_CuentaForm()

    if request.is_ajax():
        form1 = TransaccionForm(request.POST)
        if form1.is_valid():
            form1.save()
            data={
                'message':'form is saved'
            }
            return JsonResponse(data)
    else:
        form1 = TransaccionForm()

    # Contexto
    contexto = {'cuentas': cuentas, 'form': form1,'periodo': periodo,}
    return render(request, 'transaccion/transaccion.html', contexto)
