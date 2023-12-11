from django import forms
from .models import Bodega, Tipo_activo, Activo

class FormBodega(forms.ModelForm):
    class Meta:
        model = Bodega
        fields = '__all__'

class FormTipoActivo(forms.ModelForm):
    class Meta:
        model = Tipo_activo
        fields = '__all__'

class FormActivo(forms.ModelForm):
    class Meta:
        model = Activo
        fields = '__all__'