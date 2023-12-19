from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib import messages

class Bodega(models.Model):
    nombre =    models.CharField           (blank=False, null=False, max_length=50)
    ubicacion = models.CharField           (blank=False, null=False, max_length=50)
    piso =      models.IntegerField        (blank=False, null=False)
    edificio =  models.CharField           (blank=False, null=False, max_length=50)
    capacidad = models.PositiveIntegerField(blank=False, null=False)

    def __str__(self):
        return self.nombre

    def clean(self):
        if self.nombre == "Sin bodega":
            raise ValidationError("No se puede crear una bodega con el nombre 'Sin bodega'.")
        
        if self.piso < -5 or self.piso > 5:
            raise ValidationError("El piso debe estar entre -5 y 5.")
    
@receiver(pre_delete, sender=Bodega)
def prevent_delete_sin_bodega(sender, instance, **kwargs):
    if instance.nombre == "Sin bodega":
        raise ValidationError("No se puede eliminar una bodega con el nombre 'Sin bodega'.")

class Tipo_activo(models.Model):
    nombre =        models.CharField(blank=False, null=False, max_length=50)
    marca =         models.CharField(blank=False, null=False, max_length=50)
    unidad_inacap = models.CharField(blank=False, null=False, max_length=50)

    def __str__(self):
        return self.nombre
    
class Activo(models.Model):
    nombre =                models.CharField           (blank=False, null=False, verbose_name="Nombre del activo",           max_length=50)
    cantidad =              models.PositiveIntegerField(blank=False, null=False, verbose_name="Cantidad del activo")
    descripcion =           models.CharField           (blank=False, null=False, verbose_name="Descripcion del activo",      max_length=1000)
    codigo_barra =          models.CharField           (blank=False, null=False, verbose_name="Codigo de barras del activo", max_length=50)
    fecha_contable =        models.DateField           (blank=False, null=False, verbose_name="Fecha contable del activo")
    fecha_adquisicion =     models.DateField           (blank=False, null=False, verbose_name="Fecha de adquisicion del activo")
    fecha_descontinuacion = models.DateField           (blank=False, null=False, verbose_name="Fecha de descopntinuacion del activo")
    costo_alta =            models.PositiveIntegerField(blank=False, null=False, verbose_name="Costo de alta del activo")
    valor_neto =            models.IntegerField        (blank=False, null=False, verbose_name="Valor neto del activo")
    tipo_activo =           models.ForeignKey          (Tipo_activo, on_delete=models.PROTECT, blank=False, null=False)
    bodega =                models.ForeignKey          (Bodega,      on_delete=models.PROTECT, blank=False, null=False)

    def __str__(self):
        return self.nombre
    
    def clean(self):
        if self.cantidad == 0:
            raise ValidationError({'cantidad': ("La cantidad no puede ser 0.")})
        if self.fecha_adquisicion > self.fecha_descontinuacion:
            raise ValidationError({'fecha_adquisicion': ("La fecha de adquisicion no puede ser despues que la fecha de descontinuacion.")})

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
    fecha =           models.DateTimeField(blank=False, null=False)
    tipo_movimiento = models.CharField    (blank=False, null=False, max_length=5, choices=tipo_movimiento_CHOICES, default='Defau')
    activo_id =       models.ForeignKey   (Activo,      on_delete=models.PROTECT, blank=True,  null=True)
    bodega_id =       models.ForeignKey   (Bodega,      on_delete=models.PROTECT, blank=True,  null=True)
    tipo_activo_id =  models.ForeignKey   (Tipo_activo, on_delete=models.PROTECT, blank=True,  null=True)
    user =            models.ForeignKey   (User,        on_delete=models.PROTECT, blank=False, null=False)

    def __str__(self):
        tipo_movimiento = dict(self.tipo_movimiento_CHOICES).get(self.tipo_movimiento, 'Desconocido')
        if self.tipo_movimiento in ['AD_ac', 'ED_ac', 'DE_ac', 'AD_ab', 'ED_ab', 'DE_ab']:
            return f'{self.fecha} - {tipo_movimiento} - {self.activo_id.nombre}'
        elif self.tipo_movimiento in ['AD_bo', 'ED_bo', 'DE_bo']:
            return f'{self.fecha} - {tipo_movimiento} - {self.bodega_id.nombre}'
        elif self.tipo_movimiento in ['AD_ta', 'ED_ta', 'DE_ta']:
            return f'{self.fecha} - {tipo_movimiento} - {self.tipo_activo_id.nombre}'
        else:
            return f'{self.fecha} - {tipo_movimiento}'