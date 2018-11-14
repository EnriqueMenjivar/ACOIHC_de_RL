from django import forms
from apps.contabilidad_costos.models import *

class EmpleadoForms(forms.ModelForm):
	
	class Meta:
		model = Empleado

		fields = [
		'nombre_empleado',
		'apellido_empleado',
		'dui_empleado',
		'Nisss_empleado',
		'Nafp_empleado',
		'cargo_empleado',
		'años_empleado',
		]

		labels = {
		'nombre_empleado' : 'Nombres',
		'apellido_empleado' : 'Apellidos',
		'dui_empleado' : 'DUI',
		'Nisss_empleado': 'ISSS',
		'Nafp_empleado' : 'AFP',
		'cargo_empleado' : 'Cargo',
		'años_empleado' : 'Años Laborales'
		}

		widgets = {
		'nombre_empleado' : forms.TextInput(attrs={'class':'form-control'}),
		'apellido_empleado' : forms.TextInput(attrs={'class':'form-control'}),
		'dui_empleado' : forms.TextInput(attrs={'class':'form-control'}),
		'Nisss_empleado': forms.TextInput(attrs={'class':'form-control'}),
		'Nafp_empleado' : forms.TextInput(attrs={'class':'form-control'}),
		'cargo_empleado' : forms.Select(attrs={'class':'form-control'}),
		'años_empleado' : forms.TextInput(attrs={'class':'form-control'}),
		}


