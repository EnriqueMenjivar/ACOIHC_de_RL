from django.shortcuts import render, redirect
from apps.transaccion.forms import TransaccionForm, Transaccion_CuentaForm
from apps.periodo.models import Periodo
from apps.catalogo.models import CuentaHija
from apps.contabilidad_general.models import Transaccion, Transaccion_Cuenta
from django.http import JsonResponse
from decimal import Decimal

# Create your views here.


def iniciar_transaccion(request, form1):
    form1 = TransaccionForm(request.POST)
    if form1.is_valid():
        form1.save()
        tran = Transaccion.objects.latest('id')
        data = {'message': tran.id}
        return JsonResponse(data)
    else:
        form1 = TransaccionForm()


def transaccion(request):
    cuentas = CuentaHija.objects.all()
    periodo = Periodo.objects.get(estado_periodo=False)
    cuentasDebe = []
    cuentasHaber = []

    form1 = TransaccionForm()
    if request.is_ajax():
        iniciar_transaccion(request, form1)

    if 'cargar' in request.GET:
        for c in cuentas:
            if str(c.id)+"debe" in request.GET:
                if request.GET[str(c.id)+"debe"] == 'on':
                    cuentasDebe.append(c)

    if 'abonar' in request.GET:
        for c in cuentas:
            if str(c.id)+"haber" in request.GET:
                if request.GET[str(c.id)+"haber"] == 'on':
                    cuentasHaber.append(c)

            if str(c.id)+"habers" in request.GET:
                if request.GET[str(c.id)+"habers"] == 'on':
                    cuentasDebe.append(c)

    if 'guardar' in request.POST:
        for c in cuentas:
            if str(c.id)+"deb" in request.POST:
                valor = request.POST[str(c.id)+"deb"]
                t = Transaccion.objects.latest('id')
                tran = Transaccion_Cuenta(
                    transaccion_tc=t, cuenta_tc=c,
                    debe_tc=Decimal(valor),
                    haber_tc=Decimal("0.0"),
                )
                tran.save()

            if str(c.id)+"abon" in request.POST:
                valor = request.POST[str(c.id)+"abon"]
                t = Transaccion.objects.latest('id')
                tran = Transaccion_Cuenta(
                    transaccion_tc=t, cuenta_tc=c,
                    debe_tc=Decimal("0.0"),
                    haber_tc=Decimal(valor),
                )
                tran.save()

        return redirect('transaccion:transacciones')

    # Contexto
    contexto = {'cuentas': cuentas, 'form': form1, 'periodo': periodo,
                'cuentasdebe': cuentasDebe, 'cuentashaber': cuentasHaber}
    return render(request, 'transaccion/transaccion.html', contexto)


def compra_inventario(request):
    periodo = Periodo.objects.get(estado_periodo=False)
    form1 = TransaccionForm()
    if request.is_ajax():
        iniciar_transaccion(request, form1)
    
    contexto={
        'form':form1,'periodo':periodo
    }
    return render(request, 'transaccion/transaccion_especial.html',contexto)
