from django.shortcuts import render, redirect
from apps.transaccion.forms import TransaccionForm, Transaccion_CuentaForm
from apps.periodo.models import Periodo
from apps.catalogo.models import CuentaHija
from apps.contabilidad_general.models import Transaccion, Transaccion_Cuenta
from django.http import JsonResponse
from decimal import Decimal
from apps.contabilidad_costos.peps import *

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
    cuentas = CuentaHija.objects.select_related().all()
    periodo = Periodo.objects.latest('id')
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
                aumentar_saldo(c.id, valor, True)

            if str(c.id)+"abon" in request.POST:
                valor = request.POST[str(c.id)+"abon"]
                t = Transaccion.objects.latest('id')
                tran = Transaccion_Cuenta(
                    transaccion_tc=t, cuenta_tc=c,
                    debe_tc=Decimal("0.0"),
                    haber_tc=Decimal(valor),
                )
                tran.save()
                aumentar_saldo(c.id, valor, False)

        return redirect('transaccion:transacciones')

    # Contexto
    contexto = {'cuentas': cuentas, 'form': form1, 'periodo': periodo,
                'cuentasdebe': cuentasDebe, 'cuentashaber': cuentasHaber}
    return render(request, 'transaccion/transaccion.html', contexto)


def compra_inventario(request):
    cuentas = CuentaHija.objects.select_related().all()
    periodo = Periodo.objects.latest('id')
    form1 = TransaccionForm()
    if request.is_ajax():
        iniciar_transaccion(request, form1)

    if 'guardar' in request.POST:

        t = Transaccion.objects.latest('id')
        # Cargado
        c = CuentaHija.objects.get(nombre_cuenta=request.POST['cuenta'])
        totalCompra = request.POST['total']
        iva = request.POST['iva']
        precio_uni = request.POST['precio_unit']
        cant = request.POST['cantidad']

        cv = list()
        cv = peps(periodo.id, t.fecha_transaccion, c.id,int(cant),float(precio_uni), False, cv)
        

        tran = Transaccion_Cuenta(
            transaccion_tc=t,
            cuenta_tc=c,
            debe_tc=Decimal(totalCompra),
            haber_tc=Decimal("0.0"),
        )
        tran.save()
        aumentar_saldo(c.id, totalCompra, True)

        tran1 = Transaccion_Cuenta(
            transaccion_tc=t,
            cuenta_tc=CuentaHija.objects.get(id=24),
            debe_tc=Decimal(iva),
            haber_tc=Decimal("0.0"),
        )
        tran1.save()
        aumentar_saldo(24, iva, True)
        if 'efectivo0' in request.POST and 'cxp0' in request.POST:
            if request.POST['efectivo0'] == 'on' and request.POST['cxp0'] == 'on':
                efectivo = request.POST['efectivo']
                cxp = request.POST['cxp']

                tran = Transaccion_Cuenta(
                    transaccion_tc=t,
                    cuenta_tc=CuentaHija.objects.get(id=1),
                    debe_tc=Decimal("0.0"),
                    haber_tc=Decimal(efectivo),
                )
                tran.save()
                aumentar_saldo(1, efectivo, False)

                tran1 = Transaccion_Cuenta(
                    transaccion_tc=t,
                    cuenta_tc=CuentaHija.objects.get(id=137),
                    debe_tc=Decimal("0.0"),
                    haber_tc=Decimal(cxp),
                )
                tran1.save()
                aumentar_saldo(137, cxp, False)
        else:
            if 'efectivo0' in request.POST:
                if request.POST['efectivo0'] == 'on':
                    efectivo = request.POST['efectivo']
                    tran = Transaccion_Cuenta(
                        transaccion_tc=t,
                        cuenta_tc=CuentaHija.objects.get(id=1),
                        debe_tc=Decimal("0.0"),
                        haber_tc=Decimal(efectivo),
                    )
                    tran.save()
                    aumentar_saldo(1, efectivo, False)

            else:
                cxp = request.POST['cxp']
                tran1 = Transaccion_Cuenta(
                    transaccion_tc=t,
                    cuenta_tc=CuentaHija.objects.get(id=137),
                    debe_tc=Decimal("0.0"),
                    haber_tc=Decimal(cxp),
                )
                tran1.save()
                aumentar_saldo(137, cxp, False)

        return redirect('transaccion:transacciones')

    contexto = {
        'form': form1, 'periodo': periodo, 'cuentas': cuentas
    }
    return render(request, 'transaccion/transaccion_compra.html', contexto)


def devolucion_compra(request):
    cuentas = CuentaHija.objects.select_related().all()
    periodo = Periodo.objects.latest('id')
    form1 = TransaccionForm()
    error=False
    if request.is_ajax():
        iniciar_transaccion(request, form1)

    if 'guardar' in request.POST:

        t = Transaccion.objects.latest('id')
        # Cargado
        c = CuentaHija.objects.get(nombre_cuenta=request.POST['cuenta'])
        totalCompra = request.POST['total']
        iva = request.POST['iva']
        precio_uni = request.POST['precio_unit']
        cant = request.POST['cantidad']

        cv = list()
        cv = peps(periodo.id, t.fecha_transaccion, c.id,
                  int(cant), float(precio_uni), True, cv)
        

        if cv:
            tran = Transaccion_Cuenta(
                transaccion_tc=t,
                cuenta_tc=c,
                haber_tc=Decimal(totalCompra),
                debe_tc=Decimal("0.0"),
            )
            tran.save()
            aumentar_saldo(c.id, totalCompra, False)

            tran1 = Transaccion_Cuenta(
                transaccion_tc=t,
                cuenta_tc=CuentaHija.objects.get(id=24),
                haber_tc=Decimal(iva),
                debe_tc=Decimal("0.0"),
            )
            tran1.save()
            aumentar_saldo(24, iva, False)

            if 'efectivo0' in request.POST and 'cxp0' in request.POST:
                if request.POST['efectivo0'] == 'on' and request.POST['cxp0'] == 'on':
                    efectivo = request.POST['efectivo']
                    cxp = request.POST['cxp']

                    tran = Transaccion_Cuenta(
                        transaccion_tc=t,
                        cuenta_tc=CuentaHija.objects.get(id=1),
                        haber_tc=Decimal("0.0"),
                        debe_tc=Decimal(efectivo),
                    )
                    tran.save()
                    aumentar_saldo(1, efectivo, True)

                    tran1 = Transaccion_Cuenta(
                        transaccion_tc=t,
                        cuenta_tc=CuentaHija.objects.get(id=137),
                        haber_tc=Decimal("0.0"),
                        debe_tc=Decimal(cxp),
                    )
                    tran1.save()
                    aumentar_saldo(137, cxp, True)
            else:
                if 'efectivo0' in request.POST:
                    if request.POST['efectivo0'] == 'on':
                        efectivo = request.POST['efectivo']
                        tran = Transaccion_Cuenta(
                            transaccion_tc=t,
                            cuenta_tc=CuentaHija.objects.get(id=1),
                            haber_tc=Decimal("0.0"),
                            debe_tc=Decimal(efectivo),
                        )
                        tran.save()
                        aumentar_saldo(1, efectivo, True)

                else:
                    cxp = request.POST['cxp']
                    tran1 = Transaccion_Cuenta(
                        transaccion_tc=t,
                        cuenta_tc=CuentaHija.objects.get(id=137),
                        haber_tc=Decimal("0.0"),
                        debe_tc=Decimal(cxp),
                    )
                    tran1.save()
                    aumentar_saldo(137, cxp, True)

            return redirect('transaccion:transacciones')
        else:
            error = True
            contexto = {
                'form': form1, 'periodo': periodo, 'cuentas': cuentas, 'error': error
            }

    contexto = {
        'form': form1, 'periodo': periodo, 'cuentas': cuentas, 'error': error
    }
    return render(request, 'transaccion/transaccion_devo_compra.html', contexto)


def venta(request):
    cuentas = CuentaHija.objects.select_related().all()
    periodo = Periodo.objects.latest('id')
    error = False
    form1 = TransaccionForm()
    if request.is_ajax():
        iniciar_transaccion(request, form1)

    if 'guardar' in request.POST:

        t = Transaccion.objects.latest('id')
        # Cargado
        c = CuentaHija.objects.get(nombre_cuenta=request.POST['cuenta'])
        cant = request.POST['cantidad']
        porcentaje = request.POST['porcentaje']

        cv = list()
        cv = peps(periodo.id, t.fecha_transaccion,
                  c.id, int(cant), 0, True, cv)

        

        costo = 0

        if cv:
            for v in cv:
                costo = costo+v[2]

            tran = Transaccion_Cuenta(
                transaccion_tc=t,
                cuenta_tc=c,
                haber_tc=Decimal(costo),
                debe_tc=Decimal("0.0"),
            )
            tran.save()
            aumentar_saldo(c.id, costo, False)

            tran1 = Transaccion_Cuenta(
                transaccion_tc=t,
                cuenta_tc=CuentaHija.objects.get(id=133),
                haber_tc=Decimal("0.0"),
                debe_tc=Decimal(costo),
            )
            tran1.save()
            aumentar_saldo(133, costo, True)

            total = (costo*float(porcentaje))+costo
            iva = total*0.13

            tran2 = Transaccion_Cuenta(
                transaccion_tc=t,
                cuenta_tc=CuentaHija.objects.get(id=134),
                haber_tc=Decimal(total),
                debe_tc=Decimal("0.0"),
            )
            tran2.save()
            aumentar_saldo(134, total, False)

            tran3 = Transaccion_Cuenta(
                transaccion_tc=t,
                cuenta_tc=CuentaHija.objects.get(id=97),
                haber_tc=Decimal(iva),
                debe_tc=Decimal("0.0"),
            )
            tran3.save()
            aumentar_saldo(97, iva, False)

            cuenta = request.POST['cargo']
            c = CuentaHija.objects.get(id=int(cuenta))

            if c.id == 1:
                tran = Transaccion_Cuenta(
                    transaccion_tc=t,
                    cuenta_tc=CuentaHija.objects.get(id=1),
                    haber_tc=Decimal("0.0"),
                    debe_tc=total+iva,
                )
                tran.save()
                aumentar_saldo(1, total+iva, True)

            if c.id == 138:
                tran = Transaccion_Cuenta(
                    transaccion_tc=t,
                    cuenta_tc=CuentaHija.objects.get(id=138),
                    haber_tc=Decimal("0.0"),
                    debe_tc=total+iva,
                )
                tran.save()
                aumentar_saldo(138, total+iva, True)

            return redirect('transaccion:transacciones')
        else:
            error = True
            contexto = {
                'form': form1, 'periodo': periodo, 'cuentas': cuentas, 'error': error
            }

    contexto = {
        'form': form1, 'periodo': periodo, 'cuentas': cuentas, 'error': error
    }
    return render(request, 'transaccion/transaccion_venta.html', contexto)


def compra_tangibles(request):
    cuentas = CuentaHija.objects.select_related().all()
    periodo = Periodo.objects.latest('id')
    form1 = TransaccionForm()
    if request.is_ajax():
        iniciar_transaccion(request, form1)

    if 'guardar' in request.POST:

        t = Transaccion.objects.latest('id')
        # Cargado
        c = CuentaHija.objects.get(nombre_cuenta=request.POST['cuenta'])
        totalCompra = request.POST['total']
        iva = request.POST['iva']
        precio_uni = request.POST['precio_unit']
        cant = request.POST['cantidad']

        tran = Transaccion_Cuenta(
            transaccion_tc=t,
            cuenta_tc=c,
            debe_tc=Decimal(totalCompra),
            haber_tc=Decimal("0.0"),
        )
        tran.save()
        aumentar_saldo(c.id, totalCompra, True)

        tran1 = Transaccion_Cuenta(
            transaccion_tc=t,
            cuenta_tc=CuentaHija.objects.get(id=24),
            debe_tc=Decimal(iva),
            haber_tc=Decimal("0.0"),
        )
        tran1.save()
        aumentar_saldo(24, iva, True)
        if 'efectivo0' in request.POST and 'cxp0' in request.POST:
            if request.POST['efectivo0'] == 'on' and request.POST['cxp0'] == 'on':
                efectivo = request.POST['efectivo']
                cxp = request.POST['cxp']

                tran = Transaccion_Cuenta(
                    transaccion_tc=t,
                    cuenta_tc=CuentaHija.objects.get(id=1),
                    debe_tc=Decimal("0.0"),
                    haber_tc=Decimal(efectivo),
                )
                tran.save()
                aumentar_saldo(1, efectivo, False)

                tran1 = Transaccion_Cuenta(
                    transaccion_tc=t,
                    cuenta_tc=CuentaHija.objects.get(id=137),
                    debe_tc=Decimal("0.0"),
                    haber_tc=Decimal(cxp),
                )
                tran1.save()
                aumentar_saldo(137, cxp, False)
        else:
            if 'efectivo0' in request.POST:
                if request.POST['efectivo0'] == 'on':
                    efectivo = request.POST['efectivo']
                    tran = Transaccion_Cuenta(
                        transaccion_tc=t,
                        cuenta_tc=CuentaHija.objects.get(id=1),
                        debe_tc=Decimal("0.0"),
                        haber_tc=Decimal(efectivo),
                    )
                    tran.save()
                    aumentar_saldo(1, efectivo, False)

            else:
                cxp = request.POST['cxp']
                tran1 = Transaccion_Cuenta(
                    transaccion_tc=t,
                    cuenta_tc=CuentaHija.objects.get(id=137),
                    debe_tc=Decimal("0.0"),
                    haber_tc=Decimal(cxp),
                )
                tran1.save()
                aumentar_saldo(137, cxp, False)

        return redirect('transaccion:transacciones')

    contexto = {
        'form': form1, 'periodo': periodo, 'cuentas': cuentas
    }
    return render(request, 'transaccion/transaccion_compra_tangibles.html', contexto)


def venta_tangibles(request):
    cuentas = CuentaHija.objects.select_related().all()
    periodo = Periodo.objects.latest('id')
    form1 = TransaccionForm()
    if request.is_ajax():
        iniciar_transaccion(request, form1)

    if 'guardar' in request.POST:

        t = Transaccion.objects.latest('id')
        # Cargado
        c = CuentaHija.objects.get(nombre_cuenta=request.POST['cuenta'])
        totalCompra = request.POST['total']
        iva = request.POST['iva']
        precio_uni = request.POST['precio_unit']
        cant = request.POST['cantidad']

        tran = Transaccion_Cuenta(
            transaccion_tc=t,
            cuenta_tc=c,
            haber_tc=Decimal(totalCompra),
            debe_tc=Decimal("0.0"),
        )
        tran.save()
        aumentar_saldo(c.id, totalCompra, False)

        tran1 = Transaccion_Cuenta(
            transaccion_tc=t,
            cuenta_tc=CuentaHija.objects.get(id=97),
            haber_tc=Decimal(iva),
            debe_tc=Decimal("0.0"),
        )
        tran1.save()
        aumentar_saldo(97, iva, False)

        if 'efectivo0' in request.POST and 'cxp0' in request.POST:
            if request.POST['efectivo0'] == 'on' and request.POST['cxp0'] == 'on':
                efectivo = request.POST['efectivo']
                cxp = request.POST['cxp']

                tran = Transaccion_Cuenta(
                    transaccion_tc=t,
                    cuenta_tc=CuentaHija.objects.get(id=1),
                    haber_tc=Decimal("0.0"),
                    debe_tc=Decimal(efectivo),
                )
                tran.save()
                aumentar_saldo(1, efectivo, True)

                tran1 = Transaccion_Cuenta(
                    transaccion_tc=t,
                    cuenta_tc=CuentaHija.objects.get(id=138),
                    haber_tc=Decimal("0.0"),
                    debe_tc=Decimal(cxp),
                )
                tran1.save()
                aumentar_saldo(138, cxp, True)
        else:
            if 'efectivo0' in request.POST:
                if request.POST['efectivo0'] == 'on':
                    efectivo = request.POST['efectivo']
                    tran = Transaccion_Cuenta(
                        transaccion_tc=t,
                        cuenta_tc=CuentaHija.objects.get(id=1),
                        haber_tc=Decimal("0.0"),
                        debe_tc=Decimal(efectivo),
                    )
                    tran.save()
                    aumentar_saldo(1, efectivo, True)

            else:
                cxp = request.POST['cxp']
                tran1 = Transaccion_Cuenta(
                    transaccion_tc=t,
                    cuenta_tc=CuentaHija.objects.get(id=138),
                    haber_tc=Decimal("0.0"),
                    debe_tc=Decimal(cxp),
                )
                tran1.save()
                aumentar_saldo(138, cxp, True)

        return redirect('transaccion:transacciones')

    contexto = {
        'form': form1, 'periodo': periodo, 'cuentas': cuentas
    }
    return render(request, 'transaccion/transaccion_venta_tangibles.html', contexto)


def aumentar_saldo(id_cuenta, monto, opcion):
    cuenta = CuentaHija.objects.get(id=id_cuenta)
    if opcion:
        cuenta.debe = cuenta.debe+float(monto)
    else:
        cuenta.haber = cuenta.haber+float(monto)

    if cuenta.debe == cuenta.haber:
        cuenta.saldo_deudor_cuenta = 0
        cuenta.saldo_acreedor_cuenta = 0
    else:
        if cuenta.debe > cuenta.haber:
            cuenta.saldo_deudor_cuenta = cuenta.debe-cuenta.haber
        else:
            cuenta.saldo_acreedor_cuenta = cuenta.haber-cuenta.debe
    cuenta.save()
