from django.db import models
from django.contrib.auth.models import User

class Tipo_transaccion(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
    
class Bodega(models.Model):
    nombre = models.CharField(max_length=50)
    ubicacion = models.CharField(max_length=50)
    piso = models.IntegerField()
    edificio = models.CharField(max_length=50)
    capacidad = models.IntegerField()

    def __str__(self):
        return self.nombre
    
class Tipo_activo(models.Model):
    nombre = models.CharField(max_length=50)
    marca = models.CharField(max_length=50)
    unidad_inacap = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
    
class Activo(models.Model):
    nombre = models.CharField(max_length=50)
    cantidad = models.IntegerField()
    descripcion = models.CharField(max_length=1000)
    codigo_barra = models.CharField(max_length=50)
    fecha_contable = models.DateField()
    fecha_adquisicion = models.DateField()
    vida_util_total = models.IntegerField()
    vida_util_restante = models.IntegerField()
    costo_alta = models.IntegerField()
    valor_neto = models.IntegerField()
    id_tipo_activo = models.ForeignKey(Tipo_activo, on_delete=models.CASCADE)
    id_bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Movimiento_activo(models.Model):
    fecha = models.DateField()
    cantidad = models.IntegerField()
    activo = models.ForeignKey(Activo, on_delete=models.CASCADE)
    id_tipo_activo = models.ForeignKey(Tipo_activo, on_delete=models.CASCADE)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.fecha