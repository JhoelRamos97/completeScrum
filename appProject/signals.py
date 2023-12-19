from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Bodega

@receiver(post_migrate)
def create_sin_bodega(sender, **kwargs):
    if Bodega.objects.filter(nombre="Sin bodega").exists():
        return

    Bodega.objects.create(
        nombre="Sin bodega",
        ubicacion="No aplica",
        piso=0,
        edificio="No aplica",
        capacidad=0
    )