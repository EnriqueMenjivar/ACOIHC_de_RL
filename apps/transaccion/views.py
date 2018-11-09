from django.shortcuts import render
from apps.transaccion.forms import TransaccionForm, Transaccion_CuentaForm
from apps.periodo.models import Periodo
from apps.catalogo.models import Cuenta

# Create your views here.


def transaccion(request):
    cuentas = Cuenta.objects.all()
    periodo = Periodo.objects.get(estado_periodo=False)

    if request.method == 'POST':
        form = TransaccionForm(request.POST)

        if form.is_valid():
            form.save()
    else:
        form = TransaccionForm()

    # Contexto
    contexto = {'cuentas': cuentas, 'form': form,'periodo': periodo,}
    return render(request, 'transaccion/transaccion.html', contexto)
