from django import forms
from apps.periodo.models import *

class NotaForms(forms.ModelForm):
	
	class Meta:
		model = NotaPeriodo

		fields = [
		'titulo_nota',
		'descripcion_nota',
		'periodo_nota',
		]

		labels = {
		'titulo_nota': 'Titulo',
		'descripcion_nota' : 'Descripcion',
		'periodo_nota' : 'periodo',
		}

		widgets = {
		'titulo_nota': forms.TextInput(attrs={'class':'form-control'}),
		'descripcion_nota' : forms.TextInput(attrs={'class':'form-control'}),
		'periodo_nota' : forms.TextInput(attrs={'class':'form-control'}),
		}


