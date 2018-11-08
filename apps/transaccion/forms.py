from django import forms
from apps.contabilidad_general import models


class Transaccion(forms.ModelForm):
    class Meta:
        model = models.Transaccion

        fields = [
            'periodo_transaccion',
            'fecha_transaccion',
            'descripcion_transaccion',
        ]

        labels = {
            'periodo_transaccion':'Periodo',
            'fecha_transaccion':'Fecha',
            'descripcion_transaccion':'Descripcion',
        }

        widgets = {
            'periodo_transaccion':forms.TextInput,
            'fecha_transaccion': forms.DateInput(),
            'descripcion_transaccion':forms.TextInput(),
        }


class Transaccion_CuentaForm(forms.ModelForm):
    class Meta:
        model = models.Transaccion_Cuenta

        fields = [
            'transaccion_tc',
            'cuenta_tc',
            'debe_tc',
            'haber_tc',
        ]

        labels = {
            'transaccion_tc':'Transaccion',
            'cuenta_tc':'Cuenta',
            'debe_tc':'Saldo Deudor',
            'haber_tc':'Saldo Acreedor',
        }

        widgets = {
            'transaccion_tc':forms.TextInput(),
            'cuenta_tc':forms.CheckboxInput(),
            'debe_tc':forms.NumberInput(),
            'haber_tc':forms.NumberInput(),
        }
