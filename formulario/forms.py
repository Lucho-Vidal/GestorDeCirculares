from django.forms import ModelForm
from .models import Circular

class CircularForm(ModelForm):
    class Meta:
        model = Circular
        fields = ['title','description','important']