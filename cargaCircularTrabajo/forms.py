from django import forms
from .models import Circular

class CircularForm(forms.ModelForm):
    class Meta:
        model = Circular
        fields = ['titulo', 'Solicitante', 'fechaInicioTrabajo','fechaFinTrabajo','ocupaVia',
                  'necesitaCorteEnergia','kmInicio','PaloInicio','estacionInicio','kmFin',
                  'paloFin','estacionFin','via','descripcion','responsable','supervisorTransporte',
                  'piloto','personalPolicial','otro','detalleOtro']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el título'}),
            'Solicitante': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el solicitante'}),
            'fechaInicioTrabajo': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'fechaFinTrabajo': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'ocupaVia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'necesitaCorteEnergia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'kmInicio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el km de inicio'}),
            'PaloInicio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el palo de inicio'}),
            'estacionInicio': forms.Select(attrs={'class': 'form-select'}),
            'kmFin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el km de fin'}),
            'paloFin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el palo de fin'}),
            'estacionFin': forms.Select(attrs={'class': 'form-select'}),
            'via': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la vía'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ingrese la descripción'}),
            'responsable': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'supervisorTransporte': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'piloto': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'personalPolicial': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'otro': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'detalleOtro': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ingrese detalles'}),
        }
        def clean_detalleOtro(self):
            detalleOtro = self.cleaned_data.get("detalleOtro", "").strip()
            return detalleOtro if detalleOtro else None  # Guarda None si está vacío
