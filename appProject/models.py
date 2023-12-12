from django.db import models
from django.contrib.auth.models import User

class Bodega(models.Model):
    nombre = models.CharField(max_length=50, blank=False, null=False)
    ubicacion = models.CharField(max_length=50, blank=False, null=False)
    piso = models.IntegerField(blank=False, null=False)
    edificio = models.CharField(max_length=50, blank=False, null=False)
    capacidad = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return self.nombre
    
class Tipo_activo(models.Model):
    nombre = models.CharField(max_length=50, blank=False, null=False)
    marca = models.CharField(max_length=50, blank=True, null=True)
    unidad_inacap = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nombre
    
class Activo(models.Model):
    nombre = models.CharField(max_length=50, blank=False, null=False)
    cantidad = models.PositiveIntegerField(blank=False, null=False)
    descripcion = models.CharField(max_length=1000, blank=False, null=False)
    codigo_barra = models.CharField(max_length=50, blank=True, null=True)
    fecha_contable = models.DateField()
    fecha_adquisicion = models.DateField()
    vida_util_total = models.PositiveIntegerField()
    vida_util_restante = models.IntegerField()
    costo_alta = models.IntegerField()
    valor_neto = models.IntegerField()
    tipo_activo = models.ForeignKey(Tipo_activo, on_delete=models.CASCADE)
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Movimiento(models.Model):
    tipo_movimiento_CHOICES = [
        ('Defau', 'Termino defaul, no usar o hubo un error'),
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
    nombre_activo = models.CharField(max_length=50, blank=False, null=True)
    cantidad = models.PositiveIntegerField(blank=True, null=True)
    nombre_bodega = models.CharField(max_length=50, blank=False, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return self.fecha