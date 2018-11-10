from django.shortcuts import render,redirect
from apps.transaccion.forms import TransaccionForm, Transaccion_CuentaForm
from apps.periodo.models import Periodo
from apps.catalogo.models import Cuenta
from apps.contabilidad_general.models import Transaccion
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
            tran=Transaccion.objects.latest('id')
            data={
                'message': tran.id
            }
            return JsonResponse(data)
    else:
        form1 = TransaccionForm()
    
    if request.method=='POST':
        form2=Transaccion_CuentaForm(request.POST)
        if form2.is_valid():
            form2.save()
        else:
            form2=Transaccion_CuentaForm()

    # Contexto
    contexto = {'cuentas': cuentas, 'form': form1,'periodo': periodo,'form2':form2,}
    return render(request, 'transaccion/transaccion.html', contexto)