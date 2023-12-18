from django.contrib import admin
from .models import Activo, Bodega, Tipo_activo, Movimiento
# Register your models here.

@admin.register(Activo)
class ActivoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cantidad', 'descripcion', 'codigo_barra', 'fecha_contable', 'fecha_adquisicion', 'fecha_descontinuacion', 'tipo_activo', 'bodega')

@admin.register(Bodega)
class BodegaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ubicacion', 'piso', 'edificio', 'capacidad')

@admin.register(Tipo_activo)
class Tipo_activoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca', 'unidad_inacap')

@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'tipo_movimiento', 'activo_id', 'bodega_id', 'tipo_activo_id','user')