from django.contrib import admin
from .models import Activo, Bodega, Tipo_activo, Tipo_transaccion, Movimiento_activo
# Register your models here.

@admin.register(Activo)
class ActivoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cantidad', 'descripcion', 'codigo_barra', 'fecha_contable', 'fecha_adquisicion', 'vida_util_total', 'vida_util_restante', 'costo_alta', 'valor_neto', 'id_tipo_activo', 'id_bodega')

@admin.register(Bodega)
class BodegaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ubicacion', 'piso', 'edificio', 'capacidad')

@admin.register(Tipo_activo)
class Tipo_activoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'marca', 'unidad_inacap')

@admin.register(Tipo_transaccion)
class Tipo_transaccionAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Movimiento_activo)
class Movimiento_activoAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'cantidad', 'activo', 'id_tipo_activo', 'id_user')