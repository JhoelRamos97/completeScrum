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
    nombre =                models.CharField           (blank=False, null=False, verbose_name="Nombre del activo",      max_length=50)
    cantidad =              models.PositiveIntegerField(blank=False, null=False, verbose_name="Cantidad del activo")
    descripcion =           models.CharField           (blank=False, null=False, verbose_name="Descripcion del activo", max_length=1000)
    codigo_barra =          models.CharField           (blank=False, null=False, verbose_name="Codigo de barras del activo", max_length=50)
    fecha_adquisicion =     models.DateField           (blank=False, null=False, verbose_name="Fecha de adquisicion del activo")
    fecha_contable =        models.DateField           (blank=False, null=False, verbose_name="Fecha contable del activo")
    fecha_descontinuacion = models.DateField           (blank=False, null=False, verbose_name="Fecha de descopntinuacion del activo")
    costo_alta =            models.PositiveIntegerField(blank=False, null=False, verbose_name="Costo de alta del activo")
    valor_neto =            models.IntegerField        (blank=False, null=False, verbose_name="Valor neto del activo")
    tipo_activo =           models.ForeignKey          (Tipo_activo, on_delete=models.PROTECT, blank=False, null=False)

    def __str__(self):
        return self.nombre
    
    def clean_fields(self, exclude=None):
        super(Activo, self).clean_fields(exclude=exclude)
        if self.codigo_barra.isdigit() == False:
            raise ValidationError({'codigo_barra': ("El codigo de barras solo puede contener numeros.")})
    
    def clean(self):
        if self.cantidad == 0:
            raise ValidationError({'cantidad': ("La cantidad no puede ser 0.")})
        if self.costo_alta == 0:
            raise ValidationError({'costo_alta': ("El costo de alta no puede ser 0.")})
        if self.valor_neto == 0:
            raise ValidationError({'valor_neto': ("El valor neto no puede ser 0.")})
        if self.fecha_adquisicion > self.fecha_descontinuacion:
            raise ValidationError({'fecha_adquisicion': ("La fecha de adquisicion no puede ser despues que la fecha de descontinuacion.")})
        if self.fecha_contable < self.fecha_adquisicion:
            raise ValidationError({'fecha_contable': ("La fecha contable no puede ser anterior a la fecha de adquisición.")})

class Activo_bodega(models.Model):
    estado = models.BooleanField(blank=False, null=False, default=True)
    activo = models.ForeignKey(Activo, on_delete=models.PROTECT, blank=False, null=False)
    bodega = models.ForeignKey(Bodega, on_delete=models.PROTECT, blank=False, null=False)

    def __str__(self):
        return f'{self.activo.nombre} - {self.bodega.nombre}'

class Movimiento(models.Model):
    tipo_movimiento_CHOICES = [
        ('DF', 'Movimiento desconocido'),
        ('AS', 'Se agrego un activo pero sin bodega'),
        ('ES', 'Se dejo al activo sin bodega'),
        ('AD', 'Se agrego un activo a una bodega'),
        ('ED', 'Se movio un activo de una bodega a otra bodega'),
        ('DE', 'Se quito un activo de una bodega')
    ]
    fecha           = models.DateTimeField       (blank=False, null=False)
    tipo_movimiento = models.CharField           (blank=False, null=False, max_length=2, choices=tipo_movimiento_CHOICES, default='Defau')
    cantidad        = models.PositiveIntegerField(blank=False, null=False)
    activo_bodega   = models.ForeignKey          (Activo_bodega, on_delete=models.PROTECT, blank=False, null=False)
    user            = models.ForeignKey          (User,          on_delete=models.PROTECT, blank=False, null=False)

    def __str__(self):
        return f'{self.tipo_movimiento} - {self.activo_bodega} - {self.user}'