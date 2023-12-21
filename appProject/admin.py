from django.contrib import admin
from .models import Activo, Bodega, Tipo_activo, Movimiento, Activo_bodega
# Register your models here.

@admin.register(Activo)
class ActivoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cantidad', 'descripcion', 'codigo_barra', 'fecha_contable', 'fecha_adquisicion', 'fecha_descontinuacion', 'tipo_activo')

@admin.register(Bodega)
class BodegaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ubicacion', 'piso', 'edificio', 'capacidad')

@admin.register(Tipo_activo)
class Tipo_activoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca', 'unidad_inacap')

@admin.register(Activo_bodega)
class Activo_bodegaAdmin(admin.ModelAdmin):
    list_display = ('activo_id', 'bodega_id', 'estado')

@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'tipo_movimiento', 'cantidad', 'activo_bodega', 'user')