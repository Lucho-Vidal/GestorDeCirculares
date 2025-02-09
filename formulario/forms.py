from django import forms
from .models import Circular

class CircularForm(forms.ModelForm):
    class Meta:
        model = Circular
        fields = ['title', 'description', 'important']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el título'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Ingrese la descripción'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }