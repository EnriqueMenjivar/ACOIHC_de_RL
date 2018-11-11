from django import forms
from apps.catalogo.models import Grupo, Agrupacion, Cuenta, CuentaHija

class CuentaForm(forms.ModelForm):

	class Meta:
		model = Cuenta
		fields = (
			'agrupacion',
			'nombre_cuenta',
			'descripcion_cuenta'
		)

		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.fields['agrupacion'].queryset = Agrupacion.objects.none()

		labels = {
			'agrupacion':'Agrupacion',
			'nombre_cuenta':'Nombre de la cuenta',
			'descripcion_cuenta':'Descripción de la cuenta',
		}

		widgets = {
			'agrupacion': forms.Select(attrs={'class':'form-control'}),
			'nombre_cuenta': forms.TextInput(),
			'descripcion_cuenta': forms.TextInput(),
		}

		

class AgrupacionForm(forms.ModelForm):

	class Meta:
		model = Agrupacion
		fields = [
			'codigo_grup',
			'nombre_agrupacion',
			'codigo_agrupacion',
		]

		labels = {
			'codigo_grup': 'Código del grupo',
			'nombre_agrupacion':'Nombre de la agrupación',
			'codigo_agrupacion':'Código de la agrupación',
		}

		widgets = {
			'codigo_grup': forms.Select(attrs={'class':'form-control'}),
			'nombre_agrupacion': forms.TextInput(),
			'codigo_agrupacion': forms.TextInput(),
		}

class HijaForm(forms.ModelForm):

	class Meta:
		model = CuentaHija
		fields = [
			'codigo_cuenta',
			'nombre_cuenta',
			'descripcion_cuenta',
		]