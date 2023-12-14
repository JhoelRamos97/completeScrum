from django.db import models
from django.contrib.auth.models import User

class Bodega(models.Model):
    nombre = models.CharField(max_length=50, blank=False, null=False)
    ubicacion = models.CharField(max_length=50, blank=False, null=False)
    piso = models.IntegerField(blank=False, null=False)
    edificio = models.CharField(max_length=50, blank=False, null=False)
    capacidad = models.PositiveIntegerField(blank=False, null=False)

    def __str__(self):
        return self.nombre
    
class Tipo_activo(models.Model):
    nombre = models.CharField(max_length=50, blank=False, null=False)
    marca = models.CharField(max_length=50, blank=False, null=False)
    unidad_inacap = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.nombre
    
class Activo(models.Model):
    nombre = models.CharField(max_length=50, blank=False, null=False)
    cantidad = models.PositiveIntegerField(blank=False, null=False)
    descripcion = models.CharField(max_length=1000, blank=False, null=False)
    codigo_barra = models.CharField(max_length=50, blank=False, null=False)
    fecha_contable = models.DateField(blank=False, null=False)
    fecha_adquisicion = models.DateField(blank=False, null=False)
    fecha_descontinuacion = models.DateField(blank=False, null=False)
    costo_alta = models.PositiveIntegerField(blank=False, null=False)
    valor_neto = models.PositiveIntegerField(blank=False, null=False)
    tipo_activo = models.ForeignKey(Tipo_activo, on_delete=models.PROTECT, blank=True, null=True)
    bodega = models.ForeignKey(Bodega, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Movimiento(models.Model):
    tipo_movimiento_CHOICES = [
        ('Defau', 'Movimiento desconocido'),
        ('AD_ac', 'Se agrego un activo al inventario'),
        ('ED_ac', 'Se actualizo un activo en inventario'),
        ('DE_ac', 'Se elimino un activo del inventario'),
        ('AD_bo', 'Se registro una nueva bodega'),
        ('ED_bo', 'Se actualizaron datos de una bodega'),
        ('DE_bo', 'Se elimino una bodega del registro'),
        ('AD_ta', 'Se agrego un nuevo tipo de activo'),
        ('ED_ta', 'Se actualizaron datos de un tipo de activo'),
        ('DE_ta', 'Se elimino un tipo de activo del registro'),
        ('AD_ab', 'Se agrego un activo a una bodega'),
        ('ED_ab', 'Se movio un activo de una bodega a otra bodega'),
        ('DE_ab', 'Se quito un activo de una bodega')
    ]
    fecha = models.DateTimeField(blank=False, null=False)
    tipo_movimiento = models.CharField(max_length=5, choices=tipo_movimiento_CHOICES, default='Defau', blank=False, null=False)
    nombre_activo = models.CharField(max_length=50, blank=True, null=True)
    cantidad = models.PositiveIntegerField(blank=True, null=True)
    nombre_bodega = models.CharField(max_length=50, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=False, null=False)

    def __str__(self):
        tipo_movimiento = dict(self.tipo_movimiento_CHOICES).get(self.tipo_movimiento, 'Desconocido')
        if self.tipo_movimiento in ['AD_ac', 'ED_ac', 'DE_ac', 'AD_ab', 'ED_ab', 'DE_ab']:
            return f"{self.fecha.strftime('%d/%m/%Y %H:%M:%S')} - {tipo_movimiento} - Cantidad: {self.cantidad} - Nombre del activo: {self.nombre_activo} - Nombre de la bodega: {self.nombre_bodega} - Usuario: {self.user.username}"
        elif self.tipo_movimiento in ['AD_bo', 'ED_bo', 'DE_bo']:
            return f"{self.fecha.strftime('%d/%m/%Y %H:%M:%S')} - {tipo_movimiento} - Nombre de la bodega: {self.nombre_bodega} - Usuario: {self.user.username}"
        elif self.tipo_movimiento in ['AD_ta', 'ED_ta', 'DE_ta']:
            return f"{self.fecha.strftime('%d/%m/%Y %H:%M:%S')} - {tipo_movimiento} - Usuario: {self.user.username}"
        else:
            return f"{self.fecha.strftime('%d/%m/%Y %H:%M:%S')} - Tipo de movimiento desconocido - Usuario: {self.user.username}"