from django import forms
from .models import Agenda

class AgendaForm(forms.ModelForm):
    class Meta:
        model = Agenda
        fields = ['email','apellidoYNombre', 'subGerencia','grupo', 'telefono','celular','interno']
        widgets = {
            'email': forms.TextInput(attrs={'class':'form-control','placeholder':'Email'}),
            'apellidoYNombre':forms.TextInput(attrs={'class':'form-control','placeholder':'Apellido y Nombre'}), 
            'subGerencia': forms.TextInput(attrs={'class':'form-control','placeholder':'SubGerencia'}), 
            'grupo': forms.TextInput(attrs={'class':'form-control','placeholder':'grupo'}), 
            'telefono': forms.TextInput(attrs={'class':'form-control','placeholder':'Telefono'}),
            'celular': forms.TextInput(attrs={'class':'form-control','placeholder':'Celular'}),
            'interno': forms.TextInput(attrs={'class':'form-control','placeholder':'Interno'})
        }
    telefono = forms.CharField(required=False)  # ❗ Permitir vacío
    celular = forms.CharField(required=False)
    interno = forms.CharField(required=False)
    subGerencia = forms.CharField(required=False)
    grupo = forms.CharField(required=False)