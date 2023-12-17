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
        fields = ['nombre', 'cantidad', 'descripcion', 'codigo_barra', 'fecha_contable', 'fecha_adquisicion', 'fecha_descontinuacion', 'costo_alta', 'valor_neto', 'tipo_activo', 'bodega']
        widgets = {
            'fecha_contable': forms.DateInput(attrs={'type': 'date'}),
            'fecha_adquisicion': forms.DateInput(attrs={'type': 'date'}),
            'fecha_descontinuacion': forms.DateInput(attrs={'type': 'date'}),
        }

    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label='Descripción del activo'
    )