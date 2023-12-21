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
    bodega = forms.ModelChoiceField(queryset=Bodega.objects.all(), required=True)
    class Meta:
        model = Activo
        fields = '__all__'
        widgets = {
            'fecha_adquisicion': forms.DateInput(attrs={'type': 'text'}),
            'fecha_contable': forms.DateInput(attrs={'type': 'text'}),
            'fecha_descontinuacion': forms.DateInput(attrs={'type': 'text'}),
        }

    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        label='Descripción del activo'
    )